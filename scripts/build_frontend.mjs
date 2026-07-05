import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const srcDir = path.join(root, "frontend", "src");
const outDir = path.join(root, "app", "static", "dist");
fs.mkdirSync(outDir, { recursive: true });

function banner(name) {
  return `/* Built from frontend/src/${name} at ${new Date().toISOString()} */\n`;
}

function build() {
  const css = fs.readFileSync(path.join(srcDir, "app.css"), "utf8");
  const js = fs.readFileSync(path.join(srcDir, "app.js"), "utf8");
  fs.writeFileSync(path.join(outDir, "app.css"), banner("app.css") + css);
  fs.writeFileSync(path.join(outDir, "app.js"), banner("app.js") + js);
  console.log("Built frontend assets to app/static/dist");
}

build();

if (process.argv.includes("--watch")) {
  console.log("Watching frontend/src for changes...");
  fs.watch(srcDir, { recursive: false }, () => {
    try {
      build();
    } catch (error) {
      console.error(error);
    }
  });
}
