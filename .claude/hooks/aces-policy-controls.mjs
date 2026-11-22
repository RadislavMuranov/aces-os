import fs from "node:fs";
import path from "node:path";

const DEFECT_FIELDS = {
  "BUG-001": ["RESEARCH_INVENTORY_BEFORE","RESEARCH_INVENTORY_AFTER","PRESERVED_RESEARCH_IDS","NEGATIVE_RESULTS_PRESERVED","ZERO_STATE_SCOPE"],
  "BUG-002": ["CLAIM_SOURCE","EVIDENCE_CLASS","PROMOTION_JUSTIFICATION"],
  "BUG-003": ["PRIMARY_SOURCE","PRIMARY_SOURCE_RECONSTRUCTION"],
  "BUG-004": ["HISTORICAL_STATE","CURRENT_STATE","TEMPORAL_BOUNDARY"],
  "BUG-005": ["ARTIFACT_EVIDENCE","EVENT_EVIDENCE","ARTIFACT_EVENT_SEPARATION"],
  "BUG-006": ["CONTRACT_REFERENCE","EXECUTION_REFERENCE","IMPLEMENTATION_STATE"],
  "BUG-007": ["TEST_COMMAND","TEST_RAW_OUTPUT","TEST_EXIT_CODE"],
  "BUG-008": ["REAL_FAILURE","SMALLER_ALTERNATIVES","RESIDUAL_GAP"],
  "BUG-009": ["NEGATIVE_RESULTS","EXCLUSIONS","CONTRADICTIONS"],
  "BUG-010": ["OLD_STATUS","NEW_STATUS","PROMOTION_JUSTIFICATION"],
  "BUG-011": ["INDEPENDENT_SOURCE","CHATGPT_DERIVED_SUPPORT_REMOVED","CIRCULARITY_RESULT"],
  "BUG-012": ["FALSIFICATION_ATTEMPT","DECISION_CHANGING_EVIDENCE","REMAINING_UNKNOWNS"],
  "BUG-013": ["EXTERNAL_NECESSITY_EVIDENCE","SMALLER_ALTERNATIVES","RESIDUAL_GAP"],
  "BUG-014": ["OBSERVED_FAILURE","EXISTING_CONTROL_FAILURE","DELETE_SIMPLIFY_REUSE_RESULT"],
  "BUG-015": ["CLAIMED_SCOPE","ACTUAL_SCOPE","SCOPE_DIFFERENCE"],
  "BUG-016": ["CURRENT_EVIDENCE_DECISION","HISTORICAL_EFFORT_EXCLUDED","CONTINUATION_RATIONALE"],
  "BUG-017": ["CONTRADICTIONS","UNCERTAINTY_PRESERVED","RESOLUTION_STATUS"],
  "BUG-018": ["USER_OBJECTIVE","DELIVERED_OBJECTIVE","USER_ACCEPTANCE_OR_UNCHANGED_INTENT"],
  "BUG-019": ["OLD_CLAIM","NEW_CLAIM","WHY","EVIDENCE","IMPACT"],
  "BUG-020": ["RESEARCH_INVENTORY_BEFORE","RESEARCH_INVENTORY_AFTER","PRESERVED_RESEARCH_IDS","NEGATIVE_RESULTS_PRESERVED","ZERO_STATE_SCOPE"],
  "B-129": ["RESEARCH_INVENTORY_BEFORE","RESEARCH_INVENTORY_AFTER","PRESERVED_RESEARCH_IDS","NEGATIVE_RESULTS_PRESERVED","ZERO_STATE_SCOPE"],
  "B-135": ["ABSENCE_CLAIM","SEARCH_SCOPE","SOURCES_INSPECTED","SEARCH_TERMS","COVERAGE_COMPLETENESS","UNSEARCHED_BOUNDARIES"],
  "B-136": ["CURRENT_STATE","APPLICABLE_RULES","MANDATORY_ACTIONS","FORBIDDEN_ACTIONS","MANDATORY_ACTION_EVIDENCE","OPTIONAL_NEXT_NODES","MANDATORY_ACTIONS_SATISFIED"]
};
const POLICY_ID_RE = /^(?:METHOD-SELECTION-001|AGENTS-\d{2}|SCHEMA-\d{2}|FF-\d{2}|SA-(?:\d{2}|[A-L])|BP-\d{2}|BC-\d{2}|Z-[1-8]|ITR-\d{2}|BC-I[1-8]|KMA-\d{2})$/;
function parsePairs(value) {
  const result = {};
  for (const part of String(value || "").split(";")) {
    const i = part.indexOf("=");
    if (i <= 0) continue;
    result[part.slice(0, i).trim().toUpperCase()] = part.slice(i + 1).trim();
  }
  return result;
}
const hasText = value => typeof value === "string" && value.trim().length > 0;
const oneOf = (value, values) => values.includes(String(value || "").trim().toUpperCase());

export function validateDefectControl(id, value) {
  const required = DEFECT_FIELDS[id];
  if (!required) return { ok: false, errors: ["UNKNOWN_DEFECT_ID"] };
  const pairs = parsePairs(value);
  const errors = [];
  if (pairs.RESULT !== "PASS" && pairs.RESULT !== "N/A") errors.push("RESULT must be PASS or N/A");
  if (pairs.RESULT === "N/A" && (!hasText(pairs.REASON) || !hasText(pairs.EVIDENCE))) errors.push("N/A requires REASON and EVIDENCE");
  if (pairs.RESULT === "PASS") for (const field of required) if (!hasText(pairs[field])) errors.push(field);
  if (!hasText(pairs.TEST)) errors.push("TEST");
  if (pairs.RESULT === "PASS" && !/tests\/.+\.(?:test|spec)\./i.test(pairs.TEST)) errors.push("TEST must reference a test file");
  if (pairs.RESULT === "PASS" && ["BUG-001","BUG-020","B-129"].includes(id) && !oneOf(pairs.NEGATIVE_RESULTS_PRESERVED,["YES","TRUE","PRESERVED"])) errors.push("NEGATIVE_RESULTS_PRESERVED must be YES/PRESERVED");
  if (pairs.RESULT === "PASS" && id === "BUG-002" && !oneOf(pairs.EVIDENCE_CLASS,["OBSERVED","PARTIALLY VERIFIED","HISTORICAL","HYPOTHESIZED","UNVERIFIED","UNKNOWN"])) errors.push("EVIDENCE_CLASS must use an allowed epistemic label");
  if (pairs.RESULT === "PASS" && id === "BUG-003" && !oneOf(pairs.PRIMARY_SOURCE_RECONSTRUCTION,["RECONSTRUCTED","UNAVAILABLE_CLASSIFIED_UNKNOWN","HISTORICAL_ONLY"])) errors.push("PRIMARY_SOURCE_RECONSTRUCTION must preserve unavailable/unknown state");
  if (pairs.RESULT === "PASS" && id === "BUG-015" && !oneOf(pairs.SCOPE_DIFFERENCE,["NONE","DISCLOSED","LIMITED_AND_DISCLOSED"])) errors.push("SCOPE_DIFFERENCE must be NONE or explicitly disclosed");
  if (pairs.RESULT === "PASS" && id === "BUG-005" && hasText(pairs.ARTIFACT_EVIDENCE) && pairs.ARTIFACT_EVIDENCE === pairs.EVENT_EVIDENCE) errors.push("ARTIFACT_EVIDENCE and EVENT_EVIDENCE must be independent");
  if (pairs.RESULT === "PASS" && id === "BUG-006" && hasText(pairs.CONTRACT_REFERENCE) && pairs.CONTRACT_REFERENCE === pairs.EXECUTION_REFERENCE) errors.push("CONTRACT_REFERENCE and EXECUTION_REFERENCE must be distinct");
  if (pairs.RESULT === "PASS" && id === "BUG-007" && !oneOf(pairs.TEST_EXIT_CODE,["0"])) errors.push("TEST_EXIT_CODE must be 0");
  if (pairs.RESULT === "PASS" && id === "BUG-011") {
    if (!oneOf(pairs.CHATGPT_DERIVED_SUPPORT_REMOVED,["YES","TRUE"])) errors.push("CHATGPT_DERIVED_SUPPORT_REMOVED must be YES");
    if (!oneOf(pairs.CIRCULARITY_RESULT,["INDEPENDENT"])) errors.push("CIRCULARITY_RESULT must be INDEPENDENT");
  }
  if (pairs.RESULT === "PASS" && id === "BUG-014" && !oneOf(pairs.DELETE_SIMPLIFY_REUSE_RESULT,["DELETE","SIMPLIFY","REUSE","EXISTING_SYSTEM","KEEP_WITH_JUSTIFICATION"])) errors.push("DELETE_SIMPLIFY_REUSE_RESULT must record a minimality decision");
  if (pairs.RESULT === "PASS" && id === "BUG-016" && !oneOf(pairs.HISTORICAL_EFFORT_EXCLUDED,["YES","TRUE"])) errors.push("HISTORICAL_EFFORT_EXCLUDED must be YES");
  if (pairs.RESULT === "PASS" && id === "BUG-017" && !oneOf(pairs.UNCERTAINTY_PRESERVED,["YES","TRUE"])) errors.push("UNCERTAINTY_PRESERVED must be YES");
  if (pairs.RESULT === "PASS" && id === "BUG-018" && !oneOf(pairs.USER_ACCEPTANCE_OR_UNCHANGED_INTENT,["USER_ACCEPTED","UNCHANGED","NOT_APPLICABLE"])) errors.push("USER_ACCEPTANCE_OR_UNCHANGED_INTENT must be explicit");
  if (pairs.RESULT === "PASS" && id === "B-135" && !oneOf(pairs.COVERAGE_COMPLETENESS,["COMPLETE"])) errors.push("COVERAGE_COMPLETENESS must be COMPLETE before an absence claim passes");
  if (pairs.RESULT === "PASS" && id === "B-136" && !oneOf(pairs.MANDATORY_ACTIONS_SATISFIED,["YES","TRUE"])) errors.push("MANDATORY_ACTIONS_SATISFIED must be YES before optional next nodes");
  return { ok: errors.length === 0, errors, fields: pairs };
}
const POLICY_FIELDS = {};
function mapPolicy(ids, fields) { for (const id of ids) POLICY_FIELDS[id] = fields; }
mapPolicy(["METHOD-SELECTION-001"],["METHOD SELECTION","METHOD SELECTION JUSTIFICATION"]);
mapPolicy(["AGENTS-01"],["OUTPUT LANGUAGE"]);
mapPolicy(["AGENTS-02"],["PROJECT INDEX","REPOSITORY BEFORE"]);
mapPolicy(["AGENTS-03"],["SEARCH EVIDENCE","PRIMARY SOURCE"]);
mapPolicy(["AGENTS-04"],["SECRET ACCESS AUDIT"]);
mapPolicy(["AGENTS-05"],["EVIDENCE CLASSIFICATION","VERIFICATION COMMAND","RAW OUTPUT","EXIT CODE"]);
mapPolicy(["AGENTS-06"],["REPOSITORY BEFORE","REPOSITORY AFTER","REMAINING UNKNOWNS"]);
mapPolicy(["AGENTS-07"],["ITERATION COUNT","VERIFICATION ATTEMPTS"]);
mapPolicy(["AGENTS-08"],["CANON AUTHORIZATION"]);
mapPolicy(["AGENTS-09"],["HARNESS BOUNDARY"]);
const schemaFields=[
["SCOPE AUTHORITY"],["OUTPUT LANGUAGE"],["PROJECT INDEX"],["SEARCH EVIDENCE"],["SEARCH EVIDENCE"],["INSPECTION SCOPE"],["SECRET ACCESS AUDIT"],["EXTERNAL SOURCE STATUS"],["PRIMARY SOURCE"],["DOCUMENT ROUTING"],["CLAIM EVIDENCE MAP"],["VERIFICATION COMMAND","RAW OUTPUT","EXIT CODE"],["BUG AUDIT"],["MINIMALITY"],["BUG LEARNING"],["VERDICT"],["RECOVERY ACTION"],["PROJECT STATE"],["TOKEN BUDGET"],["CONTEXT STATUS"],["ITERATION COUNT"],["OUTPUT LANGUAGE"],["ITERATION STAGES"],["HARNESS BOUNDARY"]
];
schemaFields.forEach((f,i)=>mapPolicy(["SCHEMA-"+String(i+1).padStart(2,"0")],f));
const ffFields=[
["CLAIM EVIDENCE MAP"],["CLAIM EVIDENCE MAP"],["CAUSAL CHAIN"],["MINIMALITY"],["EVIDENCE CLASSIFICATION"],["INDEPENDENCE CHECK"],["RUNTIME BOUNDARY"],["PRODUCT EVIDENCE"],["HUMAN VALUE EVIDENCE"],["MINIMALITY"],["HISTORICAL EFFORT EXCLUDED"],["GATE STATUS"],["FAILURE REGISTER"],["ARCHITECTURE ESCALATION CHECK"],["FAILURE REGISTER"],["DECISION LANGUAGE"],["RESEARCH INVENTORY BEFORE","RESEARCH INVENTORY AFTER"],["CLAIM EVIDENCE MAP"],["PRIMARY SOURCE"]
];
ffFields.forEach((f,i)=>mapPolicy(["FF-"+String(i+1).padStart(2,"0")],f));
const saFields=[
["TASK"],["VERIFICATION COMMAND"],["ITERATION STAGES"],["REPOSITORY BEFORE"],["REPOSITORY AFTER"],["BUG AUDIT"],["NEW BUG SEARCH"],["SELF AUDIT INDEPENDENCE"],["BUG REGISTER UPDATE"],["BUG SEVERITY"],["CONTRADICTIONS"],["INSPECTION SCOPE"],["ARCHITECTURE ESCALATION CHECK"],["STOP CONDITIONS"],["EVIDENCE CLASSIFICATION","VERDICT"],["REGRESSION CHECK"],["MATERIALIZATION RECORD"],["NEXT ACTION"],["FAILURE FILTER MATCH"],["VERDICT"]
];
saFields.forEach((f,i)=>mapPolicy(["SA-"+String(i+1).padStart(2,"0")],f));
const saCategoryFields=[
["EVIDENCE CLASSIFICATION","CLAIM EVIDENCE MAP"],["PRIMARY SOURCE","OBJECT OF RESEARCH"],["ARCHITECTURE ESCALATION CHECK"],["MINIMALITY"],["EVIDENCE CLASSIFICATION","CONTRADICTIONS"],["REPOSITORY BEFORE","REPOSITORY AFTER"],["VERIFICATION COMMAND","RAW OUTPUT","EXIT CODE"],["SEARCH EVIDENCE","NEW BUG SEARCH"],["HUMAN VALUE EVIDENCE"],["PRODUCT EVIDENCE","MINIMALITY"],["ITERATION COUNT","VERIFICATION ATTEMPTS"],["RECOVERY ACTION","REPOSITORY BEFORE"]
];
"ABCDEFGHIJKL".split("").forEach((x,i)=>mapPolicy(["SA-"+x],saCategoryFields[i]));
const bpFields=[
["CLAIM EVIDENCE MAP"],["EVIDENCE CLASSIFICATION"],["PRIMARY SOURCE"],["TEMPORAL STATE CHECK"],["RESEARCH INVENTORY BEFORE","RESEARCH INVENTORY AFTER"],["NEGATIVE EVIDENCE","CONTRADICTIONS"],["INDEPENDENCE CHECK"],["INSPECTION SCOPE"],["MINIMALITY"],["GOVERNANCE MINIMALITY"],["HISTORICAL EFFORT EXCLUDED"],["USER OBJECTIVE","DELIVERED OBJECTIVE"],["BUG REGISTER UPDATE"],["VERDICT"],["ENFORCEMENT BOUNDARY"]
];
bpFields.forEach((f,i)=>mapPolicy(["BP-"+String(i+1).padStart(2,"0")],f));
const bcFields=[
["CONTROL OBJECTIVE"],["CONTROL PIPELINE"],["CONTROL MATRIX"],["MATERIALIZATION RECORD"],["TRANSFORMATION INVARIANTS"],["VERIFICATION COMMAND","RAW OUTPUT","EXIT CODE"],["BUG REPRODUCTION TRACE"],["CORRECTION LEDGER"],["RESEARCH INVENTORY BEFORE","RESEARCH INVENTORY AFTER"],["RELEASE GATE"],["NON-GOALS"],["VERDICT"]
];
bcFields.forEach((f,i)=>mapPolicy(["BC-"+String(i+1).padStart(2,"0")],f));
const itrFields=[
["TASK"],["VERIFICATION COMMAND"],["ITERATION STAGES"],["REPOSITORY BEFORE","PRIMARY SOURCE"],["REPOSITORY AFTER"],["BUG AUDIT"],["NEW BUG SEARCH"],["BUG CLASSIFICATION"],["OLD CLAIM","NEW CLAIM","WHY","EVIDENCE","IMPACT"],["BUG LEARNING"],["FILTER EXPANSION DECISION"],["REGRESSION CHECK"],["EVIDENCE CLASSIFICATION"],["MINIMALITY"],["STOP CONDITIONS"],["ITERATION RECORD"],["VERDICT"],["FAILURE FILTER MATCH"],["VERDICT"]
];
itrFields.forEach((f,i)=>mapPolicy(["ITR-"+String(i+1).padStart(2,"0")],f));
const invariantFields=[
["PRIMARY SOURCE","CLAIM EVIDENCE MAP"],["OLD STATUS","NEW STATUS"],["NEGATIVE EVIDENCE","CONTRADICTIONS"],["HISTORICAL STATE","CURRENT STATE"],["INDEPENDENCE CHECK"],["INSPECTION SCOPE"],["MINIMALITY"],["CORRECTION LEDGER"]
];
invariantFields.forEach((f,i)=>mapPolicy(["BC-I"+(i+1)],f));
const kmaFields=[
["BUG REGISTER"],["EVIDENCE BOUNDARY"],["BUG REGISTER","BUG AUDIT"],["BUG SEVERITY"],["RESEARCH INVENTORY BEFORE","RESEARCH INVENTORY AFTER"],["BUG REPRODUCTION TRACE"],["EVIDENCE CLASSIFICATION"],["FREEZE BOUNDARY"]
];
kmaFields.forEach((f,i)=>mapPolicy(["KMA-"+String(i+1).padStart(2,"0")],f));
for (let i=1;i<=8;i++) mapPolicy(["Z-"+i],["PRETOOLUSE TEST EVIDENCE"]);
export const POLICY_FIELD_REQUIREMENTS = POLICY_FIELDS;

export function validatePolicyControl(id, value, recordFields = {}, baseDir = process.cwd()) {
  if (!POLICY_ID_RE.test(id)) return { ok: false, errors: ["UNKNOWN_POLICY_ID"] };
  const match = String(value || "").match(/^(PASS|N\/A)@([^#]+)#(.+)$/i);
  if (!match) return { ok: false, errors: ["Expected PASS@evidence#test or N/A@reason#test"] };
  const [, status, evidence, test] = match;
  const errors = [];
  if (!hasText(evidence)) errors.push("evidence/reason missing");
  if (!/tests\/.+\.(?:test|spec)\./i.test(test)) errors.push("test path missing");
  else if (!fs.existsSync(path.resolve(baseDir, test.replace(/\\/g, "/")))) errors.push("referenced test file does not exist");
  for (const field of (POLICY_FIELDS[id] || [])) if (!hasText(recordFields[field])) errors.push("record field "+field);
  return { ok: errors.length === 0, status: status.toUpperCase(), evidence, test, errors };
}
export function validateDefectControlSet(defectIds, controls) {
  const errors = [];
  for (const id of defectIds) {
    const result = validateDefectControl(id, controls?.[id]);
    if (!result.ok) errors.push({ id, errors: result.errors });
  }
  return errors;
}
export function validatePolicyControlSet(policyIds, controls, recordFields = {}, baseDir = process.cwd()) {
  const errors = [];
  for (const id of policyIds) {
    const result = validatePolicyControl(id, controls?.[id], recordFields, baseDir);
    if (!result.ok) errors.push({ id, errors: result.errors });
  }
  return errors;
}
export const DEFECT_CONTROL_FIELDS = DEFECT_FIELDS;
