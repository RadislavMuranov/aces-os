// Stub engine: exceeds the gate deadline.
import fs from "node:fs";

const raw = fs.readFileSync(0, "utf8");
void raw;
setTimeout(() => {
  process.exit(0);
}, 10000);
