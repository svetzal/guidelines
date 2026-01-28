#!/usr/bin/env node

/**
 * Blog Image Generator
 *
 * Generates images for blog posts using OpenAI's image API.
 * Can use the character avatar as a reference to maintain visual consistency.
 * Supports multiple image types: banner (16:9), callout (1:1), diagram (9:16).
 * Takes a scene JSON specification and produces a consistent cyberpunk-styled image.
 *
 * Usage: node generate-image.mjs <scene-json-path> <output-png-path> [options]
 *
 * Options:
 *   --with-character    Use character avatar reference (default for banner)
 *   --no-character      Skip character avatar reference (default for diagram)
 *
 * Environment: Requires OPENAI_API_KEY to be set
 */

import OpenAI, { toFile } from "openai";
import { readFile, writeFile } from "fs/promises";
import { createReadStream, existsSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Character reference images for consistency - relative to repo root
const CHARACTER_REF_PATHS = [
  "assets/avatar.jpg",
  "assets/stacey.jpg",
  "assets/stacey2.jpg",
];

// Parse command line arguments
const args = process.argv.slice(2);

// Extract flags
const withCharacter = args.includes("--with-character");
const noCharacter = args.includes("--no-character");
const positionalArgs = args.filter((arg) => !arg.startsWith("--"));

if (positionalArgs.length < 2) {
  console.error(
    "Usage: node generate-image.mjs <scene-json-path> <output-png-path> [options]",
  );
  console.error("");
  console.error("Options:");
  console.error(
    "  --with-character    Use character avatar reference (default for banner)",
  );
  console.error(
    "  --no-character      Skip character avatar reference (default for diagram)",
  );
  console.error("");
  console.error("Examples:");
  console.error(
    "  node generate-image.mjs posts/2025/images/my-banner.json posts/2025/images/my-banner.png",
  );
  console.error(
    "  node generate-image.mjs posts/2025/images/diagram.json posts/2025/images/diagram.png --no-character",
  );
  console.error("");
  console.error(
    "The scene JSON should specify ImageType as 'banner', 'callout', or 'diagram'.",
  );
  console.error("Each type has a corresponding aspect ratio:");
  console.error("  - banner:  16:9 (1536x1024) - Hero image at top of article");
  console.error("  - callout: 1:1  (1024x1024) - Inline illustration");
  console.error("  - diagram: 9:16 (1024x1536) - Tall infographic");
  process.exit(1);
}

if (withCharacter && noCharacter) {
  console.error(
    "Error: Cannot specify both --with-character and --no-character",
  );
  process.exit(1);
}

const [scenePath, outputPath] = positionalArgs;

// Validate input file exists
if (!existsSync(scenePath)) {
  console.error(`Error: Scene JSON not found: ${scenePath}`);
  process.exit(1);
}

// Check for API key
if (!process.env.OPENAI_API_KEY) {
  console.error("Error: OPENAI_API_KEY environment variable not set");
  process.exit(1);
}

/**
 * Image type configurations
 */
const IMAGE_TYPES = {
  banner: {
    aspectRatio: "16:9",
    size: "1536x1024",
    description: "Hero banner at top of article",
  },
  callout: {
    aspectRatio: "1:1",
    size: "1024x1024",
    description: "Inline illustration within article",
  },
  diagram: {
    aspectRatio: "9:16",
    size: "1024x1536",
    description: "Tall infographic or process diagram",
  },
};

/**
 * Build a prompt from the scene specification
 * Passes the JSON structure directly as the prompt, with optional character reference instruction
 * @param {Object} spec - The scene specification
 * @param {boolean} useCharacter - Whether character reference image is being used
 * @param {Array} propRefs - Array of prop reference objects with propName and path
 */
function buildPrompt(spec, useCharacter = true, propRefs = []) {
  let instructions = "";

  // Character reference instruction (only for image edit mode)
  if (useCharacter) {
    instructions += "Use the provided reference images for the character. Maintain the character's appearance, face, and build exactly as shown in the character reference images.\n\n";
  }

  // Prop reference instructions
  if (propRefs.length > 0) {
    instructions += "PROP REFERENCE IMAGES: The following props have reference images provided. Render these props accurately based on their reference images:\n";
    propRefs.forEach(ref => {
      instructions += `  - ${ref.propName}: Use the provided reference image to render this prop accurately\n`;
    });
    instructions += "\n";
  }

  // Pass the JSON structure directly as the prompt
  const jsonPrompt = JSON.stringify(spec, null, 2);

  return instructions + jsonPrompt;
}

/**
 * Get image size from image type
 */
function getImageSize(spec) {
  const imageType = spec.ImageType || "banner";
  const typeConfig = IMAGE_TYPES[imageType];

  if (!typeConfig) {
    console.warn(`Unknown image type '${imageType}', defaulting to banner`);
    return IMAGE_TYPES.banner.size;
  }

  return typeConfig.size;
}

/**
 * Find all character reference files, checking multiple possible locations
 * Returns array of resolved paths that exist
 */
function findCharacterRefPaths() {
  const foundPaths = [];
  const repoRoot = path.resolve(__dirname, "../../../../");

  for (const refPath of CHARACTER_REF_PATHS) {
    // Try relative to current working directory first
    if (existsSync(refPath)) {
      foundPaths.push(refPath);
      continue;
    }

    // Try relative to script location (go up to repo root)
    const repoRefPath = path.join(repoRoot, refPath);
    if (existsSync(repoRefPath)) {
      foundPaths.push(repoRefPath);
    }
  }

  return foundPaths;
}

/**
 * Find all prop reference images from the scene specification
 * Searches in Props arrays within Scene.Environment or Situation.Props
 * Returns array of { propName, path } objects for found images
 */
function findPropRefPaths(spec, sceneJsonDir) {
  const propRefs = [];
  const repoRoot = path.resolve(__dirname, "../../../../");

  // Helper to check a single prop for ReferenceImage
  const checkProp = (prop) => {
    if (!prop.ReferenceImage) return;

    const refPath = prop.ReferenceImage;
    let resolvedPath = null;

    // Try relative to scene JSON directory first
    const relativeToScene = path.join(sceneJsonDir, refPath);
    if (existsSync(relativeToScene)) {
      resolvedPath = relativeToScene;
    }
    // Try relative to current working directory
    else if (existsSync(refPath)) {
      resolvedPath = refPath;
    }
    // Try relative to repo root
    else {
      const repoRefPath = path.join(repoRoot, refPath);
      if (existsSync(repoRefPath)) {
        resolvedPath = repoRefPath;
      }
    }

    if (resolvedPath) {
      propRefs.push({
        propName: prop.Item || prop.Name || 'unknown prop',
        path: resolvedPath
      });
    } else {
      console.warn(`Warning: Prop reference image not found: ${refPath}`);
    }
  };

  // Check Scene.Environment.Props (array format used in current banner)
  if (spec.Scene?.Environment?.Props) {
    const props = spec.Scene.Environment.Props;
    if (Array.isArray(props)) {
      props.forEach(checkProp);
    }
  }

  // Check Situation.Props (object with Character, Article, Environment arrays)
  if (spec.Situation?.Props) {
    const situationProps = spec.Situation.Props;
    ['Character', 'Article', 'Environment'].forEach(category => {
      if (Array.isArray(situationProps[category])) {
        situationProps[category].forEach(checkProp);
      }
    });
  }

  return propRefs;
}

/**
 * Determine whether to use character reference based on flags and image type
 */
function shouldUseCharacter(imageType) {
  // Explicit flags take precedence
  if (withCharacter) return true;
  if (noCharacter) return false;

  // Default behavior based on image type
  // - banner: typically features the character prominently
  // - callout: depends on content (user should specify)
  // - diagram: typically abstract, no character needed
  switch (imageType) {
    case "banner":
      return true;
    case "callout":
      return false; // User can override with --with-character
    case "diagram":
      return false;
    default:
      return false;
  }
}

async function main() {
  console.log(`Reading scene specification from: ${scenePath}`);

  // Read and parse the scene JSON
  const sceneJson = await readFile(scenePath, "utf-8");
  const spec = JSON.parse(sceneJson);

  // Determine image type
  const imageType = spec.ImageType || "banner";
  const typeConfig = IMAGE_TYPES[imageType];

  if (!typeConfig) {
    console.error(`Unknown image type: ${imageType}`);
    console.error(`Valid types: ${Object.keys(IMAGE_TYPES).join(", ")}`);
    process.exit(1);
  }

  console.log(`Image type: ${imageType} (${typeConfig.description})`);

  // Determine if we should use character reference
  const useCharacter = shouldUseCharacter(imageType);
  let characterRefPaths = [];

  if (useCharacter) {
    // Find and validate character reference files
    characterRefPaths = findCharacterRefPaths();
    if (characterRefPaths.length === 0) {
      console.error(`Error: No character reference images found`);
      console.error(
        "Expected files in assets/: avatar.jpg, stacey.jpg, stacey2.jpg",
      );
      console.error(
        "Or use --no-character to generate without character reference.",
      );
      process.exit(1);
    }
    console.log(
      `Using ${characterRefPaths.length} character reference images:`,
    );
    characterRefPaths.forEach((p) => console.log(`  - ${p}`));
  } else {
    console.log("Generating without character reference");
  }

  // Find prop reference images
  const sceneJsonDir = path.dirname(path.resolve(scenePath));
  const propRefs = findPropRefPaths(spec, sceneJsonDir);
  if (propRefs.length > 0) {
    console.log(`Using ${propRefs.length} prop reference images:`);
    propRefs.forEach((ref) => console.log(`  - ${ref.propName}: ${ref.path}`));
  }

  // Determine if we need to use the edit API (have any reference images)
  const hasReferenceImages = useCharacter || propRefs.length > 0;

  // Build the prompt (pass useCharacter to adjust prompt accordingly)
  const prompt = buildPrompt(spec, useCharacter, propRefs);
  console.log("\n--- Generated Prompt ---");
  console.log(prompt);
  console.log("--- End Prompt ---\n");

  // Determine image size
  const size = getImageSize(spec);
  console.log(`Image size: ${size}`);

  // Initialize OpenAI client
  const client = new OpenAI();

  let response;

  try {
    if (hasReferenceImages) {
      console.log("Loading reference images...");

      // Collect all reference image paths
      const allRefPaths = [
        ...characterRefPaths,
        ...propRefs.map(ref => ref.path)
      ];

      // Load all reference images for the edit API
      const refFiles = await Promise.all(
        allRefPaths.map(async (refPath) => {
          const filename = path.basename(refPath);
          const ext = path.extname(refPath).toLowerCase();
          const mimeType = ext === '.png' ? 'image/png' : 'image/jpeg';
          return toFile(createReadStream(refPath), filename, {
            type: mimeType,
          });
        }),
      );

      console.log(`Loaded ${refFiles.length} reference images (${characterRefPaths.length} character, ${propRefs.length} prop)`);
      console.log("Generating image via OpenAI Image Edit API...");

      response = await client.images.edit({
        model: "gpt-image-1.5",
        image: refFiles,
        prompt: prompt,
        n: 1,
        size: size,
      });
    } else {
      console.log("Generating image via OpenAI Image Generate API...");

      response = await client.images.generate({
        model: "gpt-image-1.5",
        prompt: prompt,
        n: 1,
        size: size,
      });
    }

    console.log("API Response received");

    // Handle response
    const imageData = response.data[0];

    if (imageData.b64_json) {
      // Handle base64 response
      console.log("Received base64 image data");
      const imageBuffer = Buffer.from(imageData.b64_json, "base64");
      await writeFile(outputPath, imageBuffer);
    } else if (imageData.url) {
      // Handle URL response
      console.log(`Fetching image from URL...`);
      const imageResponse = await fetch(imageData.url);
      const imageBuffer = Buffer.from(await imageResponse.arrayBuffer());
      await writeFile(outputPath, imageBuffer);
    } else {
      console.error(
        "Unexpected response format:",
        JSON.stringify(imageData, null, 2),
      );
      process.exit(1);
    }

    console.log(`Image saved to: ${outputPath}`);
    console.log("Done!");
  } catch (error) {
    console.error("Error generating image:", error.message);
    if (error.response) {
      console.error("API response:", error.response.data);
    }
    process.exit(1);
  }
}

main();
