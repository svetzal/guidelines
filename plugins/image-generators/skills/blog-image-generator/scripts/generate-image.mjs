#!/usr/bin/env node

import { existsSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const DEFAULT_MODEL = "gpt-image-2.5-sunburst";
const DEFAULT_API_BASE_URL = "https://api.openai.com/v1";
const CHARACTER_REF_FILES = ["avatar.jpg", "stacey.jpg", "stacey2.jpg"];

const IMAGE_TYPES = {
  banner: {
    size: "1536x1024",
    description: "Hero banner at top of article",
    characterByDefault: true,
  },
  callout: {
    size: "1024x1024",
    description: "Inline illustration within article",
    characterByDefault: false,
  },
  diagram: {
    size: "1024x1536",
    description: "Tall infographic or process diagram",
    characterByDefault: false,
  },
};

function printUsage() {
  console.log(`
Usage: node generate-image.mjs <scene-json-path> <output-png-path> [options]

Options:
  --model <model>       OpenAI image model (default: ${DEFAULT_MODEL})
  --assets-dir <path>   Directory containing character reference images
  --with-character      Use character references (default for banners)
  --no-character        Skip character references
  --show-prompt         Print the complete generated prompt
  --force               Overwrite an existing output file
  -h, --help            Show this help

Environment:
  OPENAI_API_KEY        Required API key
  OPENAI_IMAGE_MODEL    Session-wide model override
  OPENAI_BASE_URL       API base URL (default: ${DEFAULT_API_BASE_URL})
`);
}

function fail(message) {
  console.error(`Error: ${message}`);
  process.exit(1);
}

function parseArgs(args) {
  const options = {
    assetsDir: null,
    force: false,
    model: process.env.OPENAI_IMAGE_MODEL || DEFAULT_MODEL,
    noCharacter: false,
    positional: [],
    showPrompt: false,
    withCharacter: false,
  };

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];

    if (arg === "-h" || arg === "--help") {
      printUsage();
      process.exit(0);
    }

    if (arg === "--with-character") {
      options.withCharacter = true;
    } else if (arg === "--no-character") {
      options.noCharacter = true;
    } else if (arg === "--show-prompt") {
      options.showPrompt = true;
    } else if (arg === "--force") {
      options.force = true;
    } else if (arg === "--model" || arg === "--assets-dir") {
      const value = args[index + 1];
      if (!value || value.startsWith("--")) fail(`${arg} requires a value`);
      if (arg === "--model") options.model = value;
      if (arg === "--assets-dir") options.assetsDir = value;
      index += 1;
    } else if (arg.startsWith("--model=")) {
      options.model = arg.slice("--model=".length);
    } else if (arg.startsWith("--assets-dir=")) {
      options.assetsDir = arg.slice("--assets-dir=".length);
    } else if (arg.startsWith("--")) {
      fail(`unknown option: ${arg}`);
    } else {
      options.positional.push(arg);
    }
  }

  if (!options.model) fail("--model requires a value");
  if (options.assetsDir === "") fail("--assets-dir requires a value");
  if (options.withCharacter && options.noCharacter) {
    fail("cannot specify both --with-character and --no-character");
  }
  if (options.positional.length !== 2) {
    printUsage();
    fail("expected a scene JSON path and output PNG path");
  }

  const [scenePath, outputPath] = options.positional;
  return { ...options, scenePath, outputPath };
}

function ancestorDirectories(startPath) {
  const directories = [];
  let current = path.resolve(startPath);

  while (true) {
    directories.push(current);
    const parent = path.dirname(current);
    if (parent === current) return directories;
    current = parent;
  }
}

function unique(paths) {
  return [...new Set(paths.map((candidate) => path.resolve(candidate)))];
}

function firstExisting(paths) {
  return unique(paths).find((candidate) => existsSync(candidate));
}

function findCharacterRefPaths(sceneDirectory, explicitAssetsDir) {
  const assetDirectories = explicitAssetsDir
    ? [path.resolve(explicitAssetsDir)]
    : unique([
        path.join(process.cwd(), "assets"),
        ...ancestorDirectories(sceneDirectory).map((directory) =>
          path.join(directory, "assets"),
        ),
      ]);

  return CHARACTER_REF_FILES.flatMap((filename) => {
    const found = firstExisting(
      assetDirectories.map((directory) => path.join(directory, filename)),
    );
    return found ? [found] : [];
  });
}

function collectProps(spec) {
  const props = [];

  if (Array.isArray(spec.Scene?.Environment?.Props)) {
    props.push(...spec.Scene.Environment.Props);
  }

  for (const category of ["Character", "Article", "Environment"]) {
    const categoryProps = spec.Situation?.Props?.[category];
    if (Array.isArray(categoryProps)) props.push(...categoryProps);
  }

  return props;
}

function findPropRefPaths(spec, sceneDirectory) {
  const ancestors = ancestorDirectories(sceneDirectory);

  return collectProps(spec).flatMap((prop) => {
    if (!prop.ReferenceImage) return [];

    const found = firstExisting([
      path.join(sceneDirectory, prop.ReferenceImage),
      path.resolve(process.cwd(), prop.ReferenceImage),
      ...ancestors.map((directory) =>
        path.join(directory, prop.ReferenceImage),
      ),
    ]);

    if (!found) {
      console.warn(`Warning: prop reference not found: ${prop.ReferenceImage}`);
      return [];
    }

    return [{ propName: prop.Item || prop.Name || "unknown prop", path: found }];
  });
}

function buildPrompt(spec, useCharacter, propRefs) {
  const instructions = [];

  if (useCharacter) {
    instructions.push(
      "Use the provided reference images for the character. Maintain the character's appearance, face, and build exactly as shown in the character reference images.",
    );
  }

  if (propRefs.length > 0) {
    instructions.push(
      "PROP REFERENCE IMAGES:\n" +
        propRefs
          .map(
            ({ propName }) =>
              `- ${propName}: render this prop accurately from its reference image`,
          )
          .join("\n"),
    );
  }

  instructions.push(JSON.stringify(spec, null, 2));
  return instructions.join("\n\n");
}

function mimeTypeFor(filePath) {
  return path.extname(filePath).toLowerCase() === ".png"
    ? "image/png"
    : "image/jpeg";
}

async function requestOpenAI(endpoint, apiKey, body, headers = {}) {
  const baseUrl = (process.env.OPENAI_BASE_URL || DEFAULT_API_BASE_URL).replace(
    /\/+$/,
    "",
  );
  const response = await fetch(`${baseUrl}/${endpoint}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}`, ...headers },
    body,
  });
  const responseText = await response.text();

  let payload;
  try {
    payload = JSON.parse(responseText);
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const detail = payload?.error?.message || responseText || response.statusText;
    throw new Error(`OpenAI API returned ${response.status}: ${detail}`);
  }

  if (!payload) throw new Error("OpenAI API returned a non-JSON response");
  return payload;
}

async function editImage(apiKey, model, prompt, size, referencePaths) {
  const form = new FormData();
  form.append("model", model);
  form.append("prompt", prompt);
  form.append("n", "1");
  form.append("size", size);

  for (const referencePath of referencePaths) {
    const image = await readFile(referencePath);
    form.append(
      "image[]",
      new Blob([image], { type: mimeTypeFor(referencePath) }),
      path.basename(referencePath),
    );
  }

  return requestOpenAI("images/edits", apiKey, form);
}

async function generateImage(apiKey, model, prompt, size) {
  return requestOpenAI(
    "images/generations",
    apiKey,
    JSON.stringify({ model, prompt, n: 1, size }),
    { "Content-Type": "application/json" },
  );
}

async function saveImage(response, outputPath) {
  const imageData = response.data?.[0];
  if (!imageData) throw new Error("OpenAI API response contained no image");

  let imageBuffer;
  if (imageData.b64_json) {
    imageBuffer = Buffer.from(imageData.b64_json, "base64");
  } else if (imageData.url) {
    const imageResponse = await fetch(imageData.url);
    if (!imageResponse.ok) {
      throw new Error(`image download returned ${imageResponse.status}`);
    }
    imageBuffer = Buffer.from(await imageResponse.arrayBuffer());
  } else {
    throw new Error("OpenAI API response had no image data or URL");
  }

  await mkdir(path.dirname(path.resolve(outputPath)), { recursive: true });
  await writeFile(outputPath, imageBuffer);
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const { scenePath, outputPath } = options;

  if (!existsSync(scenePath)) fail(`scene JSON not found: ${scenePath}`);
  if (existsSync(outputPath) && !options.force) {
    fail(`output already exists: ${outputPath} (use --force to overwrite)`);
  }

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) fail("OPENAI_API_KEY is not set");

  const spec = JSON.parse(await readFile(scenePath, "utf8"));
  const imageType = spec.ImageType || "banner";
  const typeConfig = IMAGE_TYPES[imageType];
  if (!typeConfig) {
    fail(
      `unknown image type '${imageType}'; use ${Object.keys(IMAGE_TYPES).join(", ")}`,
    );
  }

  const useCharacter = options.withCharacter
    ? true
    : options.noCharacter
      ? false
      : typeConfig.characterByDefault;
  const sceneDirectory = path.dirname(path.resolve(scenePath));
  const characterRefs = useCharacter
    ? findCharacterRefPaths(sceneDirectory, options.assetsDir)
    : [];

  if (useCharacter && characterRefs.length === 0) {
    fail(
      "no character references found; run from the content repository, use --assets-dir, or use --no-character",
    );
  }
  if (useCharacter && characterRefs.length < CHARACTER_REF_FILES.length) {
    console.warn(
      `Warning: found ${characterRefs.length} of ${CHARACTER_REF_FILES.length} character references`,
    );
  }

  const propRefs = findPropRefPaths(spec, sceneDirectory);
  const referencePaths = [
    ...characterRefs,
    ...propRefs.map(({ path: propPath }) => propPath),
  ];
  const prompt = buildPrompt(spec, useCharacter, propRefs);

  console.log(`Scene: ${scenePath}`);
  console.log(`Type: ${imageType} — ${typeConfig.description}`);
  console.log(`Model: ${options.model}`);
  console.log(`Size: ${typeConfig.size}`);
  console.log(`References: ${referencePaths.length}`);
  if (options.showPrompt) {
    console.log(`\n--- Prompt ---\n${prompt}\n--- End prompt ---\n`);
  }

  const response = referencePaths.length
    ? await editImage(
        apiKey,
        options.model,
        prompt,
        typeConfig.size,
        referencePaths,
      )
    : await generateImage(apiKey, options.model, prompt, typeConfig.size);

  await saveImage(response, outputPath);
  console.log(`Saved: ${outputPath}`);
}

main().catch((error) =>
  fail(error instanceof Error ? error.message : String(error)),
);
