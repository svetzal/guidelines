#!/usr/bin/env node

/**
 * Create a labeled image grid from a set of images.
 *
 * Usage:
 *   node create-grid.mjs <output.jpg> --rows "label1,label2,..." --cols "label1,label2,..." --images "path1,path2,..."
 *
 * Images should be provided in row-major order (left to right, top to bottom).
 *
 * Example:
 *   node create-grid.mjs grid.jpg \
 *     --rows "Cyberpunk,Girl Next Door,Goth,Professional" \
 *     --cols "Cyberpunk,Coffeeshop,Winter Forest,Boardroom" \
 *     --images "img1.png,img2.png,img3.png,..."
 *
 * Options:
 *   --size        Grid size in pixels (default: 4096)
 *   --header      Header size in pixels for labels (default: 80)
 *   --font-size   Font size for labels (default: 32)
 *   --quality     JPEG quality 1-100 (default: 90)
 */

import { createCanvas, loadImage, registerFont } from 'canvas';
import { writeFileSync } from 'fs';
import { resolve } from 'path';

function parseArgs(args) {
  const result = {
    output: null,
    rows: [],
    cols: [],
    images: [],
    size: 4096,
    header: 80,
    fontSize: 32,
    quality: 90
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];

    if (arg === '--rows') {
      result.rows = args[++i].split(',').map(s => s.trim());
    } else if (arg === '--cols') {
      result.cols = args[++i].split(',').map(s => s.trim());
    } else if (arg === '--images') {
      result.images = args[++i].split(',').map(s => s.trim());
    } else if (arg === '--size') {
      result.size = parseInt(args[++i], 10);
    } else if (arg === '--header') {
      result.header = parseInt(args[++i], 10);
    } else if (arg === '--font-size') {
      result.fontSize = parseInt(args[++i], 10);
    } else if (arg === '--quality') {
      result.quality = parseInt(args[++i], 10);
    } else if (!arg.startsWith('--') && !result.output) {
      result.output = arg;
    }
    i++;
  }

  return result;
}

async function createGrid(options) {
  const { output, rows, cols, images, size, header, fontSize, quality } = options;

  if (!output) {
    console.error('Error: Output file path required');
    process.exit(1);
  }

  if (rows.length === 0 || cols.length === 0) {
    console.error('Error: Both --rows and --cols are required');
    process.exit(1);
  }

  const expectedImages = rows.length * cols.length;
  if (images.length !== expectedImages) {
    console.error(`Error: Expected ${expectedImages} images (${rows.length} rows x ${cols.length} cols), got ${images.length}`);
    process.exit(1);
  }

  console.log(`Creating ${size}x${size} grid with ${rows.length} rows and ${cols.length} cols`);

  // Calculate dimensions
  const contentWidth = size - header;  // Space for row labels on left
  const contentHeight = size - header; // Space for column labels on top
  const cellWidth = Math.floor(contentWidth / cols.length);
  const cellHeight = Math.floor(contentHeight / rows.length);

  console.log(`Cell size: ${cellWidth}x${cellHeight}`);

  // Create canvas
  const canvas = createCanvas(size, size);
  const ctx = canvas.getContext('2d');

  // Fill background
  ctx.fillStyle = '#1a1a2e';
  ctx.fillRect(0, 0, size, size);

  // Configure text
  ctx.fillStyle = '#ffffff';
  ctx.font = `bold ${fontSize}px sans-serif`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  // Draw column headers
  for (let c = 0; c < cols.length; c++) {
    const x = header + c * cellWidth + cellWidth / 2;
    const y = header / 2;
    ctx.fillText(cols[c], x, y);
  }

  // Draw row headers (rotated)
  for (let r = 0; r < rows.length; r++) {
    const x = header / 2;
    const y = header + r * cellHeight + cellHeight / 2;

    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(rows[r], 0, 0);
    ctx.restore();
  }

  // Draw grid lines
  ctx.strokeStyle = '#333355';
  ctx.lineWidth = 2;

  // Vertical lines
  for (let c = 0; c <= cols.length; c++) {
    const x = header + c * cellWidth;
    ctx.beginPath();
    ctx.moveTo(x, header);
    ctx.lineTo(x, size);
    ctx.stroke();
  }

  // Horizontal lines
  for (let r = 0; r <= rows.length; r++) {
    const y = header + r * cellHeight;
    ctx.beginPath();
    ctx.moveTo(header, y);
    ctx.lineTo(size, y);
    ctx.stroke();
  }

  // Header separator lines
  ctx.strokeStyle = '#555577';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(header, 0);
  ctx.lineTo(header, size);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(0, header);
  ctx.lineTo(size, header);
  ctx.stroke();

  // Load and draw images
  let imageIndex = 0;
  for (let r = 0; r < rows.length; r++) {
    for (let c = 0; c < cols.length; c++) {
      const imagePath = images[imageIndex];
      const cellX = header + c * cellWidth;
      const cellY = header + r * cellHeight;

      try {
        console.log(`Loading image ${imageIndex + 1}/${images.length}: ${imagePath}`);
        const img = await loadImage(resolve(imagePath));

        // Calculate scaling to fit cell while maintaining aspect ratio
        const imgAspect = img.width / img.height;
        const cellAspect = cellWidth / cellHeight;

        let drawWidth, drawHeight, drawX, drawY;

        if (imgAspect > cellAspect) {
          // Image is wider than cell - fit to width
          drawWidth = cellWidth - 4; // 2px padding on each side
          drawHeight = drawWidth / imgAspect;
          drawX = cellX + 2;
          drawY = cellY + (cellHeight - drawHeight) / 2;
        } else {
          // Image is taller than cell - fit to height
          drawHeight = cellHeight - 4;
          drawWidth = drawHeight * imgAspect;
          drawX = cellX + (cellWidth - drawWidth) / 2;
          drawY = cellY + 2;
        }

        ctx.drawImage(img, drawX, drawY, drawWidth, drawHeight);
      } catch (err) {
        console.error(`Error loading image ${imagePath}: ${err.message}`);
        // Draw error placeholder
        ctx.fillStyle = '#442222';
        ctx.fillRect(cellX + 2, cellY + 2, cellWidth - 4, cellHeight - 4);
        ctx.fillStyle = '#ff6666';
        ctx.font = `${fontSize * 0.6}px sans-serif`;
        ctx.fillText('Error', cellX + cellWidth / 2, cellY + cellHeight / 2);
        ctx.font = `bold ${fontSize}px sans-serif`;
        ctx.fillStyle = '#ffffff';
      }

      imageIndex++;
    }
  }

  // Save as JPEG
  const buffer = canvas.toBuffer('image/jpeg', { quality: quality / 100 });
  writeFileSync(resolve(output), buffer);
  console.log(`Grid saved to: ${output}`);
}

// Main
const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  console.log(`
Usage: node create-grid.mjs <output.jpg> [options]

Options:
  --rows "label1,label2,..."    Row labels (required)
  --cols "label1,label2,..."    Column labels (required)
  --images "path1,path2,..."    Image paths in row-major order (required)
  --size <pixels>               Grid size (default: 4096)
  --header <pixels>             Header size for labels (default: 80)
  --font-size <pixels>          Font size for labels (default: 32)
  --quality <1-100>             JPEG quality (default: 90)

Images should be provided in row-major order (left to right, top to bottom).
`);
  process.exit(0);
}

const options = parseArgs(args);
createGrid(options).catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
