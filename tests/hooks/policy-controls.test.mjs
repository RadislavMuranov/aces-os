import assert from "node:assert/strict";
import test from "node:test";
import {
  DEFECT_CONTROL_FIELDS,
  POLICY_FIELD_REQUIREMENTS,
  validateDefectControl,
  validatePolicyControl
} from "../../.claude/hooks/aces-policy-controls.mjs";
import { REQUIRED_DEFECT_IDS, REQUIRED_POLICY_IDS } from "../../.claude/hooks/aces-hook-engine.mjs";

function validFieldValue(id,field,i) {
  const fixed = {
    NEGATIVE_RESULTS_PRESERVED:"YES",
    EVIDENCE_CLASS:"UNKNOWN",
    PRIMARY_SOURCE_RECONSTRUCTION:"UNAVAILABLE_CLASSIFIED_UNKNOWN",
    SCOPE_DIFFERENCE:"DISCLOSED",
    ARTIFACT_EVIDENCE:"artifact:source-a",
    EVENT_EVIDENCE:"event:source-b",
    ARTIFACT_EVENT_SEPARATION:"SEPARATE",
    CONTRACT_REFERENCE:"contract:spec-a",
    EXECUTION_REFERENCE:"execution:run-b",
    IMPLEMENTATION_STATE:"OBSERVED",
    TEST_EXIT_CODE:"0",
    CHATGPT_DERIVED_SUPPORT_REMOVED:"YES",
    CIRCULARITY_RESULT:"INDEPENDENT",
    DELETE_SIMPLIFY_REUSE_RESULT:"REUSE",
    HISTORICAL_EFFORT_EXCLUDED:"YES",
    UNCERTAINTY_PRESERVED:"YES",
    USER_ACCEPTANCE_OR_UNCHANGED_INTENT:"UNCHANGED",
    COVERAGE_COMPLETENESS:"COMPLETE",
    MANDATORY_ACTIONS_SATISFIED:"YES"
  };
  return fixed[field] || "evidence-"+id+"-"+(i+1);
}
function validDefectValue(id) {
  const fields = DEFECT_CONTROL_FIELDS[id];
  return ["RESULT=PASS", ...fields.map((field,i)=>field+"="+validFieldValue(id,field,i)), "TEST=tests/hooks/policy-controls.test.mjs"].join("; ");
}

for (const id of REQUIRED_DEFECT_IDS) {
  test("defect control "+id+" accepts a complete evidence-backed PASS",()=>{
    const result=validateDefectControl(id,validDefectValue(id));
    assert.equal(result.ok,true,JSON.stringify(result.errors));
  });
  test("defect control "+id+" rejects missing rule-specific evidence",()=>{
    const fields=DEFECT_CONTROL_FIELDS[id];
    const broken=validDefectValue(id).replace(fields[0]+"="+validFieldValue(id,fields[0],0),"");
    const result=validateDefectControl(id,broken);
    assert.equal(result.ok,false);
    assert.ok(result.errors.includes(fields[0]));
  });
}
test("defect-specific semantic invariants reject invalid evidence",()=>{
  assert.equal(validateDefectControl("BUG-002",validDefectValue("BUG-002").replace("EVIDENCE_CLASS=UNKNOWN","EVIDENCE_CLASS=MADE_UP")).ok,false);
  assert.equal(validateDefectControl("BUG-003",validDefectValue("BUG-003").replace("PRIMARY_SOURCE_RECONSTRUCTION=UNAVAILABLE_CLASSIFIED_UNKNOWN","PRIMARY_SOURCE_RECONSTRUCTION=ASSUMED")).ok,false);
  assert.equal(validateDefectControl("BUG-015",validDefectValue("BUG-015").replace("SCOPE_DIFFERENCE=DISCLOSED","SCOPE_DIFFERENCE=HIDDEN")).ok,false);
  assert.equal(validateDefectControl("BUG-005",validDefectValue("BUG-005").replace("EVENT_EVIDENCE=event:source-b","EVENT_EVIDENCE=artifact:source-a")).ok,false);
  assert.equal(validateDefectControl("BUG-006",validDefectValue("BUG-006").replace("EXECUTION_REFERENCE=execution:run-b","EXECUTION_REFERENCE=contract:spec-a")).ok,false);
  assert.equal(validateDefectControl("BUG-007",validDefectValue("BUG-007").replace("TEST_EXIT_CODE=0","TEST_EXIT_CODE=1")).ok,false);
  assert.equal(validateDefectControl("BUG-011",validDefectValue("BUG-011").replace("CIRCULARITY_RESULT=INDEPENDENT","CIRCULARITY_RESULT=DEPENDENT")).ok,false);
  assert.equal(validateDefectControl("BUG-014",validDefectValue("BUG-014").replace("DELETE_SIMPLIFY_REUSE_RESULT=REUSE","DELETE_SIMPLIFY_REUSE_RESULT=UNKNOWN")).ok,false);
  assert.equal(validateDefectControl("BUG-016",validDefectValue("BUG-016").replace("HISTORICAL_EFFORT_EXCLUDED=YES","HISTORICAL_EFFORT_EXCLUDED=NO")).ok,false);
  assert.equal(validateDefectControl("BUG-017",validDefectValue("BUG-017").replace("UNCERTAINTY_PRESERVED=YES","UNCERTAINTY_PRESERVED=NO")).ok,false);
  assert.equal(validateDefectControl("BUG-018",validDefectValue("BUG-018").replace("USER_ACCEPTANCE_OR_UNCHANGED_INTENT=UNCHANGED","USER_ACCEPTANCE_OR_UNCHANGED_INTENT=UNKNOWN")).ok,false);
  assert.equal(validateDefectControl("B-135",validDefectValue("B-135").replace("COVERAGE_COMPLETENESS=COMPLETE","COVERAGE_COMPLETENESS=PARTIAL")).ok,false);
  assert.equal(validateDefectControl("B-136",validDefectValue("B-136").replace("MANDATORY_ACTIONS_SATISFIED=YES","MANDATORY_ACTIONS_SATISFIED=NO")).ok,false);
});
test("defect N/A requires a reason, evidence and a test reference",()=>{
  assert.equal(validateDefectControl("BUG-018","RESULT=N/A; REASON=No relevant intent change; EVIDENCE=scope record; TEST=tests/hooks/policy-controls.test.mjs").ok,true);
  assert.equal(validateDefectControl("BUG-018","RESULT=N/A; REASON=No relevant intent change; TEST=tests/hooks/policy-controls.test.mjs").ok,false);
});

function validPolicyRecord(id) {
  return Object.fromEntries((POLICY_FIELD_REQUIREMENTS[id]||[]).map(field=>[field,"evidence:"+id+":"+field]));
}
for (const id of REQUIRED_POLICY_IDS) {
  test("policy section "+id+" requires its mapped evidence fields and test",()=>{
    const result=validatePolicyControl(id,"PASS@source:section "+id+"#tests/hooks/policy-controls.test.mjs",validPolicyRecord(id));
    assert.equal(result.ok,true,JSON.stringify(result.errors));
  });
  test("policy section "+id+" rejects missing rule-specific evidence",()=>{
    const fields=POLICY_FIELD_REQUIREMENTS[id]||[];
    const record=validPolicyRecord(id);
    if(fields.length) delete record[fields[0]];
    const result=validatePolicyControl(id,"PASS@source:section "+id+"#tests/hooks/policy-controls.test.mjs",record);
    assert.equal(result.ok,false);
    if(fields.length) assert.ok(result.errors.includes("record field "+fields[0]));
  });
}
test("policy control rejects a syntactically valid but nonexistent test path",()=>{
  const result=validatePolicyControl("AGENTS-05","PASS@source:AGENTS-05#tests/hooks/does-not-exist.test.mjs",validPolicyRecord("AGENTS-05"),process.cwd());
  assert.equal(result.ok,false);
  assert.ok(result.errors.includes("referenced test file does not exist"));
});
test("unknown policy IDs are rejected",()=>{
  assert.equal(validatePolicyControl("FAKE-999","PASS@source#tests/hooks/policy-controls.test.mjs").ok,false);
});
