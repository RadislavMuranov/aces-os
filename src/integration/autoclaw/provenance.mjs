// Provenance: read-only join between task envelopes and the engine's journal.
// The journal has no task_id column, so the link is line number + sha256 of the
// exact row. Nothing here writes to the journal (only the engine does).
// Design reference: aces-integration/04-design.md sections 6.4, 10.

import fs from "node:fs";
import crypto from "node:crypto";

export function sha256Hex(input) {
  return crypto.createHash("sha256").update(input).digest("hex");
}

export function readJournalRows(file) {
  if (!file || !fs.existsSync(file)) return [];
  const text = fs.readFileSync(file, "utf8");
  const lines = text.split("\n");
  if (lines.length > 0 && lines[lines.length - 1] === "") lines.pop();
  return lines.map((raw, index) => {
    const row = raw.replace(/\r$/, "");
    const parts = row.split("\t");
    return {
      line: index + 1,
      row,
      timestamp: parts[0] ?? null,
      rule_id: parts[1] ?? null,
      decision: parts[2] ?? null,
      row_sha256: sha256Hex(row),
    };
  });
}

export function journalTail(file, n = 20) {
  const limit = Math.max(0, Math.min(Number(n) || 0, 200));
  const rows = readJournalRows(file);
  return limit === 0 ? [] : rows.slice(-limit);
}

/**
 * Verify every journal reference stored in the envelope.
 * Returns {verified, checked, gaps[]} and never repairs anything.
 */
export function verifyEvents(events, journalFile) {
  const rows = readJournalRows(journalFile);
  const byLine = new Map(rows.map((r) => [r.line, r]));
  const gaps = [];
  let checked = 0;

  const checkRef = (ref, where) => {
    if (!ref || typeof ref.line !== "number") return;
    checked += 1;
    const row = byLine.get(ref.line);
    if (!row) {
      gaps.push({
        code: "JOURNAL_LINE_MISSING",
        where,
        line: ref.line,
        detail: "journal was rotated or truncated after the reference was written",
      });
      return;
    }
    if (ref.row_sha256 && row.row_sha256 !== ref.row_sha256) {
      gaps.push({
        code: "JOURNAL_HASH_MISMATCH",
        where,
        line: ref.line,
        expected: ref.row_sha256,
        actual: row.row_sha256,
      });
    }
    if (ref.rule_id && row.rule_id !== ref.rule_id) {
      gaps.push({
        code: "JOURNAL_RULE_MISMATCH",
        where,
        line: ref.line,
        expected: ref.rule_id,
        actual: row.rule_id,
      });
    }
  };

  for (let i = 0; i < events.length; i += 1) {
    const ev = events[i];
    if (ev.seq !== i + 1) {
      gaps.push({ code: "SEQ_GAP", where: `line ${i + 1}`, expected: i + 1, actual: ev.seq });
    }
    const where = `${ev.type}#${ev.seq}`;
    if (ev.type === "policy" && Array.isArray(ev.policy?.results)) {
      for (const r of ev.policy.results) checkRef(r.journal, `${where}:${r.op_id}`);
    }
    if (ev.type === "dispatch" && ev.policy) checkRef(ev.policy.journal, where);
    if (ev.type === "result" && ev.stop_gate) checkRef(ev.stop_gate.journal, where);
    if (ev.type === "close" && ev.stop_gate) checkRef(ev.stop_gate.journal, where);
  }

  return { verified: gaps.length === 0, checked, gaps, journal_lines: rows.length };
}
