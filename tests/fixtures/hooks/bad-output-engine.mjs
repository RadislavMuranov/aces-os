// Stub engine: appends an allow journal row but prints non-JSON stdout.
import fs from "node:fs";
import path from "node:path";

const raw = fs.readFileSync(0, "utf8");
const payload = JSON.parse(raw || "{}");
const journal = path.join(String(payload.cwd || "."), ".claude", "hooks", "journal.tsv");
fs.appendFileSync(journal, `${new Date().toISOString()}\tSTUB\tallow\n`, "utf8");
process.stdout.write("this is not json");
