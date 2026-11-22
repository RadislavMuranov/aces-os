import assert from "node:assert/strict";
import test from "node:test";
import fs from "node:fs";
import { REQUIRED_DEFECT_IDS, REQUIRED_POLICY_IDS } from "../../.claude/hooks/aces-hook-engine.mjs";
import { POLICY_FIELD_REQUIREMENTS } from "../../.claude/hooks/aces-policy-controls.mjs";

test("every registered defect maps to a defect-specific Stop evidence validator and regression test",()=>{
  const file=fs.readFileSync(new URL("../../.claude/policy/defect-enforcement-map.json",import.meta.url),"utf8").replace(/^\uFEFF/,"");
  const map=JSON.parse(file);
  const byId=new Map(map.entries.map(x=>[x.id,x]));
  for(const id of REQUIRED_DEFECT_IDS){
    const entry=byId.get(id);
    assert.ok(entry,"missing defect map entry "+id);
    assert.equal(entry.enforcement_point,"Stop: defect-specific evidence validator",id);
    assert.equal(entry.control_id,"DEFECT-CONTROL-"+id);
    assert.match(entry.test,/policy-controls\.test\.mjs/);
    assert.match(entry.enforcement_limit,/STRUCTURED_EVIDENCE_ONLY/);
  }
});

test("every active policy section maps to an evidence gate and positive/negative test",()=>{
  const file=fs.readFileSync(new URL("../../.claude/policy/defect-enforcement-map.json",import.meta.url),"utf8").replace(/^\uFEFF/,"");
  const map=JSON.parse(file);
  const byId=new Map(map.policy_rules.map(x=>[x.id,x]));
  assert.equal(map.policy_rules.length,REQUIRED_POLICY_IDS.length);
  assert.equal(byId.size,REQUIRED_POLICY_IDS.length);
  for(const id of REQUIRED_POLICY_IDS){
    const entry=byId.get(id);
    assert.ok(entry,"missing policy map entry "+id);
    assert.equal(entry.enforcement_point,"Stop: per-section evidence attestation validator",id);
    assert.equal(entry.control_id,"POLICY-REVIEW-"+id);
    assert.match(entry.test,/policy-controls\.test\.mjs/);
    assert.ok(POLICY_FIELD_REQUIREMENTS[id]?.length>0,"missing rule-specific evidence fields "+id);
    assert.match(entry.enforcement_limit,/REVIEW_EVIDENCE_GATE/);
  }
});
