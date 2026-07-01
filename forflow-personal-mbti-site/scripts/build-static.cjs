#!/usr/bin/env node
const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const outDir = path.join(root, "dist");
const assets = [
  "index.html",
  "styles.css",
  "data.js",
  "engine.js",
  "app.js",
  "qr-forflow-personal.png",
  "qr-forflow.jpg"
];

fs.rmSync(outDir, { recursive: true, force: true });
fs.mkdirSync(outDir, { recursive: true });

for (const asset of assets) {
  fs.copyFileSync(path.join(root, asset), path.join(outDir, asset));
}

for (const entry of fs.readdirSync(outDir)) {
  if (!assets.includes(entry)) {
    fs.rmSync(path.join(outDir, entry), { recursive: true, force: true });
  }
}

console.log(`Built ${assets.length} static assets into dist/`);
