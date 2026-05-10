import { cp, mkdir } from "node:fs/promises";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = resolve(__filename, "..");
const projectRoot = resolve(__dirname, "..");

const sourceDir = resolve(
  projectRoot,
  "node_modules",
  "onnxruntime-web",
  "dist",
);
const targetDir = resolve(projectRoot, "public", "ort");

await mkdir(targetDir, { recursive: true });
await cp(sourceDir, targetDir, { recursive: true });

console.log("Copied ONNX Runtime Web assets to public/ort");
