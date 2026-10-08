export type EpistemicState =
  | "OBSERVED"
  | "DERIVED"
  | "UNKNOWN"
  | "REJECTED";

export type DependencyState =
  | "VERIFIED"
  | "PARTIALLY_VERIFIED"
  | "UNKNOWN"
  | "BLOCKED";

export interface UnknownDisposition {
  cause: string;
  impact: string;
  required_evidence: string;
  blocks: string;
  next_action: string;
  disposition: string;
}

export interface ControlDependency {
  dependency_id: string;
  state: DependencyState;
  scope: "FULL" | "RESTRICTED";
}

export interface ControlRecord {
  mission_id: string;
  gate_id: string;
  work_item_id: string;
  action_id: string;
  source_set: string[];
  observation: string;
  evidence: string;
  epistemic_state: EpistemicState;
  scope: string;
  limitation: string;
  conclusion: string;
  unknown_disposition?: UnknownDisposition;
  dependencies?: ControlDependency[];
}

export type ControlRecordValidationResult =
  | { valid: true }
  | {
      valid: false;
      reason:
        | "INVALID_MISSION_TRACEABILITY"
        | "INVALID_EVIDENCE_LINEAGE"
        | "UNKNOWN_WITHOUT_DISPOSITION"
        | "INVALID_DEPENDENCY_ADMISSIBILITY";
    };

function nonEmpty(value: string): boolean {
  return value.trim().length > 0;
}

function hasCompleteTraceability(record: ControlRecord): boolean {
  return [
    record.mission_id,
    record.gate_id,
    record.work_item_id,
    record.action_id,
    record.observation,
    record.evidence,
    record.scope,
    record.limitation,
    record.conclusion,
  ].every(nonEmpty);
}

function hasEvidenceLineage(record: ControlRecord): boolean {
  return (
    record.source_set.length > 0 &&
    record.source_set.every(nonEmpty) &&
    nonEmpty(record.observation) &&
    nonEmpty(record.evidence)
  );
}

function hasUnknownDisposition(record: ControlRecord): boolean {
  if (record.epistemic_state !== "UNKNOWN") return true;
  const disposition = record.unknown_disposition;
  if (!disposition) return false;

  return [
    disposition.cause,
    disposition.impact,
    disposition.required_evidence,
    disposition.blocks,
    disposition.next_action,
    disposition.disposition,
  ].every(nonEmpty);
}

function hasAdmissibleDependencies(record: ControlRecord): boolean {
  for (const dependency of record.dependencies ?? []) {
    if (!nonEmpty(dependency.dependency_id)) return false;
    if (dependency.state === "UNKNOWN" || dependency.state === "BLOCKED") {
      return false;
    }
    if (
      dependency.state === "PARTIALLY_VERIFIED" &&
      dependency.scope !== "RESTRICTED"
    ) {
      return false;
    }
  }

  return true;
}

/**
 * Validates the admissibility contract of a control record.
 *
 * This function does not establish truth, authority, execution, acceptance,
 * or production readiness. It only rejects records that violate the
 * minimum control-record contract.
 */
export function validateControlRecord(
  record: ControlRecord,
): ControlRecordValidationResult {
  if (!hasCompleteTraceability(record)) {
    return { valid: false, reason: "INVALID_MISSION_TRACEABILITY" };
  }

  if (!hasEvidenceLineage(record)) {
    return { valid: false, reason: "INVALID_EVIDENCE_LINEAGE" };
  }

  if (!hasUnknownDisposition(record)) {
    return { valid: false, reason: "UNKNOWN_WITHOUT_DISPOSITION" };
  }

  if (!hasAdmissibleDependencies(record)) {
    return { valid: false, reason: "INVALID_DEPENDENCY_ADMISSIBILITY" };
  }

  return { valid: true };
}
