// Stub engine: exits 0 but writes no journal row.
import fs from "node:fs";

const raw = fs.readFileSync(0, "utf8");
void raw;
process.stdout.write(JSON.stringify({ hookSpecificOutput: { permissionDecision: "allow" } }));
