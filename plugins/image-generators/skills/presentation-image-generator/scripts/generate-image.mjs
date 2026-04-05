#!/usr/bin/env node

/**
 * Presentation Image Generator
 *
 * Generates images for Slidev presentations using OpenAI's image API.
 * Abstract-first approach: character is OFF by default for all image roles.
 * Supports multiple image roles: cover, section-break, concept, comparison,
 * diagram, background, accent.
 *
 * Usage: node generate-image.mjs <scene-json-path> <output-png-path> [options]
 *
 * Options:
 *   --with-character    Include character reference images
 *   --no-character      Explicitly skip character (default for all roles)
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
    "  --with-character    Include character reference images",
  );
  console.error(
    "  --no-character      Explicitly skip character (default for all roles)",
  );
  console.error("");
  console.error("Examples:");
  console.error(
    "  node generate-image.mjs presentations/my-talk/public/images/cover.json presentations/my-talk/public/images/cover.png",
  );
  console.error(
    "  node generate-image.mjs cover.json cover.png --with-character",
  );
  console.error("");
  console.error("Image roles and their default sizes:");
  console.error("  - cover:         16:9 (1536x1024) - Title/hero slide");
  console.error("  - section-break: 16:9 (1536x1024) - Atmospheric transition");
  console.error("  - concept:       1:1  (1024x1024) - Abstract idea visualization");
  console.error("  - comparison:    16:9 (1536x1024) - Before/after, contrast");
  console.error("  - diagram:       9:16 (1024x1536) - Process/architecture");
  console.error("  - background:    16:9 (1536x1024) - Subtle texture behind text");
  console.error("  - accent:        1:1  (1024x1024) - Small inline visual");
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
 * Image role configurations with default sizes
 */
const IMAGE_ROLES = {
  cover: {
    defaultAspectRatio: "16:9",
    defaultSize: "1536x1024",
    description: "Title/hero slide, dramatic",
  },
  "section-break": {
    defaultAspectRatio: "16:9",
    defaultSize: "1536x1024",
    description: "Atmospheric transition between sections",
  },
  concept: {
    defaultAspectRatio: "1:1",
    defaultSize: "1024x1024",
    description: "Abstract idea visualization",
  },
  comparison: {
    defaultAspectRatio: "16:9",
    defaultSize: "1536x1024",
    description: "Before/after or contrast visual",
  },
  diagram: {
    defaultAspectRatio: "9:16",
    defaultSize: "1024x1536",
    description: "Process or architecture diagram",
  },
  background: {
    defaultAspectRatio: "16:9",
    defaultSize: "1536x1024",
    description: "Subtle texture behind text",
  },
  accent: {
    defaultAspectRatio: "1:1",
    defaultSize: "1024x1024",
    description: "Small inline visual element",
  },
};

/**
 * Map aspect ratio strings to OpenAI image sizes
 */
const ASPECT_RATIO_TO_SIZE = {
  "16:9": "1536x1024",
  "1:1": "1024x1024",
  "9:16": "1024x1536",
};

/**
 * Build a prompt from the scene specification
 * @param {Object} spec - The scene specification
 * @param {boolean} useCharacter - Whether character reference image is being used
 * @param {Array} propRefs - Array of prop reference objects with propName and path
 */
function buildPrompt(spec, useCharacter = false, propRefs = []) {
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
 * Get image size from ImageRole + optional Layout.AspectRatio override
 */
function getImageSize(spec) {
  const imageRole = spec.ImageRole || "cover";
  const roleConfig = IMAGE_ROLES[imageRole];

  if (!roleConfig) {
    console.warn(`Unknown image role '${imageRole}', defaulting to cover`);
    return IMAGE_ROLES.cover.defaultSize;
  }

  // Check for aspect ratio override in Layout block
  const aspectOverride = spec.Layout?.AspectRatio;
  if (aspectOverride && ASPECT_RATIO_TO_SIZE[aspectOverride]) {
    return ASPECT_RATIO_TO_SIZE[aspectOverride];
  }

  return roleConfig.defaultSize;
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

  // Check Situation.Props (object with Character, Conceptual, Environment arrays)
  if (spec.Situation?.Props) {
    const situationProps = spec.Situation.Props;
    ['Character', 'Conceptual', 'Environment'].forEach(category => {
      if (Array.isArray(situationProps[category])) {
        situationProps[category].forEach(checkProp);
      }
    });
  }

  return propRefs;
}

/**
 * Determine whether to use character reference based on flags and spec
 * Presentation images default to NO character for all roles.
 * Character is enabled via --with-character flag or presence of Character block in spec.
 */
function shouldUseCharacter(spec) {
  // Explicit flags take precedence
  if (withCharacter) return true;
  if (noCharacter) return false;

  // If the spec includes a Character block, assume character is desired
  if (spec.Character) return true;

  // Default: no character for all presentation image roles
  return false;
}

async function main() {
  console.log(`Reading scene specification from: ${scenePath}`);

  // Read and parse the scene JSON
  const sceneJson = await readFile(scenePath, "utf-8");
  const spec = JSON.parse(sceneJson);

  // Determine image role
  const imageRole = spec.ImageRole || "cover";
  const roleConfig = IMAGE_ROLES[imageRole];

  if (!roleConfig) {
    console.error(`Unknown image role: ${imageRole}`);
    console.error(`Valid roles: ${Object.keys(IMAGE_ROLES).join(", ")}`);
    process.exit(1);
  }

  console.log(`Image role: ${imageRole} (${roleConfig.description})`);

  // Determine if we should use character reference
  const useCharacter = shouldUseCharacter(spec);
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
    console.log("Generating without character reference (abstract mode)");
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
