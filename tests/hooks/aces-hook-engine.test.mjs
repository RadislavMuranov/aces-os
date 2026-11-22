import assert from "node:assert/strict";
import test from "node:test";
import { DEFECT_CONTROL_FIELDS, POLICY_FIELD_REQUIREMENTS } from "../../.claude/hooks/aces-policy-controls.mjs";
import {
  REQUIRED_DEFECT_IDS, REQUIRED_POLICY_IDS, evaluatePreToolUse, evaluateStop, formatJournalRow
} from "../../.claude/hooks/aces-hook-engine.mjs";

const pre=(tool_name,tool_input,state)=>evaluatePreToolUse({tool_name,tool_input},state);

test("Z-1 blocks commit-hook bypass and core.hooksPath mutation; permits read",()=>{
  assert.equal(pre("Bash",{command:"git commit --no-verify -m x -- src/a.ts"}).rule,"Z-1");
  assert.equal(pre("Bash",{command:"git commit -n -m x -- src/a.ts"}).rule,"Z-1");
  assert.equal(pre("Bash",{command:"git config core.hooksPath .hooks"}).rule,"Z-1");
  assert.equal(pre("Bash",{command:"git config --get core.hooksPath"}).decision,"allow");
});
test("Z-2 blocks git stash; safe git status passes",()=>{
  assert.equal(pre("Bash",{command:"git stash pop"}).rule,"Z-2");
  assert.equal(pre("Bash",{command:"git status"}).decision,"allow");
});
test("Z-3 blocks hard reset only",()=>{
  assert.equal(pre("Bash",{command:"git reset --hard HEAD~1"}).rule,"Z-3");
  assert.equal(pre("Bash",{command:"git reset --soft HEAD~1"}).decision,"allow");
});
test("Z-4 blocks rebase; merge passes",()=>{
  assert.equal(pre("Bash",{command:"git rebase main"}).rule,"Z-4");
  assert.equal(pre("Bash",{command:"git merge main"}).decision,"allow");
});
test("Z-5 blocks force flags and '+' refspec; normal push passes",()=>{
  for(const command of ["git push --force origin main","git push --force-with-lease origin main","git push origin +main:main"])assert.equal(pre("Bash",{command}).rule,"Z-5",command);
  assert.equal(pre("Bash",{command:"git push origin main"}).decision,"allow");
});
test("Z-6 blocks broad staging; explicit path passes",()=>{
  for(const command of ["git add -A","git add .","git add -u","git add --all","git add --update"])assert.equal(pre("Bash",{command}).rule,"Z-6",command);
  assert.equal(pre("Bash",{command:"git add src/a.ts"}).decision,"allow");
});
test("Z-7 blocks pathless and -a commits; explicit pathspec passes",()=>{
  assert.equal(pre("Bash",{command:"git commit -m message"}).rule,"Z-7");
  assert.equal(pre("Bash",{command:"git commit -a -m message -- src/a.ts"}).rule,"Z-7");
  assert.equal(pre("Bash",{command:"git commit -m message -- src/a.ts"}).decision,"allow");
});
test("Z-8 blocks .env and .env.* reads; .env.example is allowed",()=>{
  assert.equal(pre("Read",{file_path:"C:\\repo\\.env"}).rule,"Z-8");
  assert.equal(pre("Read",{file_path:"C:\\repo\\.env.local"}).rule,"Z-8");
  assert.equal(pre("Read",{file_path:"C:\\repo\\.env.example"}).decision,"allow");
  assert.equal(pre("Bash",{command:"cat .env"}).rule,"Z-8");
  assert.equal(pre("PowerShell",{command:"Get-Content .env.production"}).rule,"Z-8");
  assert.equal(pre("Bash",{command:"cat .env.example"}).decision,"allow");
});
test("compound commands and pipelines are inspected",()=>{
  assert.equal(pre("Bash",{command:"git status && git stash"}).rule,"Z-2");
  assert.equal(pre("Bash",{command:"git status; git rebase main"}).rule,"Z-4");
  assert.equal(pre("Bash",{command:"git status | git stash"}).rule,"Z-2");
});
test("nested bash and PowerShell commands are inspected",()=>{
  assert.equal(pre("Bash",{command:"bash -c 'git stash'"}).rule,"Z-2");
  assert.equal(pre("PowerShell",{command:"powershell -Command \"git stash\""}).rule,"Z-2");
  assert.equal(pre("Bash",{command:"bash -c 'echo \"git stash\"'"}).decision,"allow");
});
test("shell control-flow blocks are inspected and dynamic nested commands ask",()=>{
  assert.equal(pre("Bash",{command:"if true; then git stash; fi"}).rule,"Z-2");
  assert.equal(pre("PowerShell",{command:"if ($true) { git stash }"}).rule,"Z-2");
  assert.equal(pre("Bash",{command:"bash -c \"$(echo 'git stash')\""}).decision,"ask");
});
test("BUG-001/BUG-020 require confirmation before deleting research or experiment records",()=>{
  assert.equal(pre("Bash",{command:"rm -rf knowledge/research"}).rule,"BUG-001/BUG-020");
  assert.equal(pre("Bash",{command:"git rm docs/research/source.md"}).decision,"ask");
  assert.equal(pre("PowerShell",{command:"Remove-Item -Recurse .\\knowledge\\research\\source.md"}).decision,"ask");
  assert.equal(pre("Bash",{command:"rm temp-output.txt"}).decision,"allow");
  assert.equal(pre("Bash",{command:"echo 'rm -rf knowledge/research'"}).decision,"allow");
});
test("quoted prose and comments do not trigger git rules",()=>{
  assert.equal(pre("Bash",{command:"echo \"git stash\""}).decision,"allow");
  assert.equal(pre("Bash",{command:"git status # git stash"}).decision,"allow");
  assert.equal(pre("PowerShell",{command:"Write-Output 'git stash'"}).decision,"allow");
});
test("ambiguous shell syntax asks instead of allowing",()=>{
  assert.equal(pre("Bash",{command:"git stash '"}).decision,"ask");
});
test("protected ACES files and new governance rules require confirmation",()=>{
  assert.equal(pre("Edit",{file_path:"C:\\repo\\SCHEMA.md"}).decision,"ask");
  assert.equal(pre("Write",{file_path:"C:\\repo\\spec\\MASTER-PROTOCOL.md"}).decision,"ask");
  assert.equal(pre("Edit",{file_path:"C:\\repo\\docs\\audit\\KMA-11-CHATGPT-BUG-SYSTEM.md"}).decision,"ask");
  assert.equal(pre("Write",{file_path:"C:\\repo\\spec\\governance\\new-rule.md"}).rule,"BUG-014");
  assert.equal(pre("Edit",{file_path:"C:\\repo\\src\\index.ts"}).decision,"allow");
  assert.equal(pre("Write",{file_path:"C:\\repo\\docs\\product\\note.md"}).decision,"allow");
});
test("same verification command is limited to two attempts",()=>{
  const state={verificationAttempts:{}},input={command:"node --test tests/*.test.ts"};
  assert.equal(pre("Bash",input,state).decision,"allow");
  assert.equal(pre("Bash",input,state).decision,"allow");
  assert.equal(pre("Bash",input,state).rule,"BUDGET-RETRY-2");
});
test("journal row contains no command field",()=>{
  const row=formatJournalRow("2026-11-17T10:00:00.000Z","Z-2","deny");
  assert.equal(row,"2026-11-17T10:00:00.000Z\tZ-2\tdeny\n");
  assert.equal(row.includes("git stash"),false);
});

function defectControl(id){
  const fixed={NEGATIVE_RESULTS_PRESERVED:"YES",EVIDENCE_CLASS:"UNKNOWN",PRIMARY_SOURCE_RECONSTRUCTION:"UNAVAILABLE_CLASSIFIED_UNKNOWN",SCOPE_DIFFERENCE:"DISCLOSED",ARTIFACT_EVIDENCE:"artifact:source-a",EVENT_EVIDENCE:"event:source-b",ARTIFACT_EVENT_SEPARATION:"SEPARATE",CONTRACT_REFERENCE:"contract:spec-a",EXECUTION_REFERENCE:"execution:run-b",IMPLEMENTATION_STATE:"OBSERVED",TEST_EXIT_CODE:"0",CHATGPT_DERIVED_SUPPORT_REMOVED:"YES",CIRCULARITY_RESULT:"INDEPENDENT",DELETE_SIMPLIFY_REUSE_RESULT:"REUSE",HISTORICAL_EFFORT_EXCLUDED:"YES",UNCERTAINTY_PRESERVED:"YES",USER_ACCEPTANCE_OR_UNCHANGED_INTENT:"UNCHANGED",COVERAGE_COMPLETENESS:"COMPLETE",MANDATORY_ACTIONS_SATISFIED:"YES"};
  return "CONTROL "+id+": RESULT=PASS; "+DEFECT_CONTROL_FIELDS[id].map((field,i)=>field+"="+(fixed[field]||"evidence-"+id+"-"+(i+1))).join("; ")+"; TEST=tests/hooks/policy-controls.test.mjs";
}
function validPass(){
  const baseFields=new Set(["TASK","REPOSITORY BEFORE","PRIMARY SOURCE","INSPECTION SCOPE","EVIDENCE CLASSIFICATION","NEGATIVE EVIDENCE","CONTRADICTIONS","MINIMALITY","VERIFICATION COMMAND","RAW OUTPUT","EXIT CODE","BUG AUDIT","REMAINING UNKNOWNS","REGRESSION CHECK","REPOSITORY AFTER","POLICY RULES CHECKED","VERDICT","NEXT ACTION"]);
  const policyFields=[...new Set(Object.values(POLICY_FIELD_REQUIREMENTS).flat())].filter(field=>!baseFields.has(field));
  const rows=[
    "TASK: bounded policy check",
    "REPOSITORY BEFORE: detached HEAD and dirty tree observed",
    "PRIMARY SOURCE: repository sources and Method Selection rule",
    "INSPECTION SCOPE: AGENTS, SCHEMA, governance and hooks",
    "EVIDENCE CLASSIFICATION: OBSERVED",
    "NEGATIVE EVIDENCE: none",
    "CONTRADICTIONS: none unresolved",
    "MINIMALITY: PreToolUse and Stop; Canon untouched",
    "VERIFICATION COMMAND: node --test tests/hooks/*.test.mjs",
    "RAW OUTPUT: tests 1; pass 1; fail 0",
    "EXIT CODE: 0",
    "BUG AUDIT: COMPLETE",
    "REMAINING UNKNOWNS: semantic truth is not machine-proven",
    "REGRESSION CHECK: registered defect IDs classified",
    "REPOSITORY AFTER: new hook files read back",
    "POLICY RULES CHECKED: "+REQUIRED_POLICY_IDS.map(id=>id+"=PASS@source:section "+id+"#tests/hooks/policy-controls.test.mjs").join("; "),
    "VERDICT: PASS",
    "NEXT ACTION: verify in Claude Code session",
    ...REQUIRED_DEFECT_IDS.map(id=>id+": CLEAR"),
    ...REQUIRED_DEFECT_IDS.map(defectControl),
    ...policyFields.map(field=>field+": evidence:"+field)
  ];
  return "VERDICT: PASS\n<!-- ACES_ITERATION_RECORD\n"+rows.join("\n")+"\n-->";
}
test("Stop hook blocks PASS without structured evidence",()=>{
  const r=evaluateStop({cwd:"C:\\repo\\aces-os",last_assistant_message:"VERDICT: PASS\nDone."},{turnCount:0});
  assert.equal(r.decision,"block");
});
test("Stop hook permits a complete evidence record with every defect classified",()=>{
  const result=evaluateStop({cwd:process.cwd(),last_assistant_message:validPass()},{turnCount:0});
  assert.equal(result.decision,"allow",result.reason);
});
test("Stop hook blocks each missing registered defect classification",()=>{
  for(const id of REQUIRED_DEFECT_IDS){
    const msg=validPass().replace(new RegExp("^"+id+": CLEAR$","m"),"");
    const r=evaluateStop({cwd:"C:\\repo\\aces-os",last_assistant_message:msg},{turnCount:0});
    assert.equal(r.decision,"block",id);
    assert.match(r.reason,new RegExp(id));
  }
});
test("Stop hook blocks PASS when a defect-specific evidence field is missing",()=>{
  const msg=validPass().replace("RESEARCH_INVENTORY_BEFORE=evidence-BUG-001-1","RESEARCH_INVENTORY_BEFORE=");
  const r=evaluateStop({cwd:"C:\\\\repo\\\\aces-os",last_assistant_message:msg},{turnCount:0});
  assert.equal(r.decision,"block");
  assert.match(r.reason,/CONTROL BUG-001/);
});
test("Stop hook blocks PASS when a policy section has no source-specific test trace",()=>{
  const msg=validPass().replace("SCHEMA-01=PASS@source:section SCHEMA-01#tests/hooks/policy-controls.test.mjs","SCHEMA-01=PASS@source:section SCHEMA-01#");
  const r=evaluateStop({cwd:"C:\\\\repo\\\\aces-os",last_assistant_message:msg},{turnCount:0});
  assert.equal(r.decision,"block");
  assert.match(r.reason,/POLICY SCHEMA-01/);
});
test("Stop hook blocks found or unknown defect status from PASS",()=>{
  for(const status of ["FOUND","UNKNOWN","REVIEW"]){
    const msg=validPass().replace("BUG-007: CLEAR","BUG-007: "+status);
    assert.equal(evaluateStop({cwd:"C:\\repo\\aces-os",last_assistant_message:msg},{turnCount:0}).decision,"block");
  }
});
test("Stop hook blocks every missing policy-rule classification",()=>{
  for(const id of REQUIRED_POLICY_IDS){
    const msg=validPass().replace(new RegExp(id+"=PASS@[^;]+"),"");
    const r=evaluateStop({cwd:"C:\\repo\\aces-os",last_assistant_message:msg},{turnCount:0});
    assert.equal(r.decision,"block",id);
    assert.match(r.reason,new RegExp(id));
  }
});
test("Stop hook enforces 40-turn work budget",()=>{
  const state={turnCount:39};
  assert.equal(evaluateStop({cwd:"C:\\repo\\aces-os",last_assistant_message:"Still investigating."},state).rule,"BUDGET-TURN-40");
  assert.equal(evaluateStop({cwd:"C:\\repo\\aces-os",last_assistant_message:"VERDICT: BLOCKED\nBlocker recorded."},{turnCount:39}).decision,"allow");
});
test("Stop hook does not apply to unrelated repositories",()=>{
  assert.equal(evaluateStop({cwd:"C:\\repo\\other",last_assistant_message:"VERDICT: PASS"},{turnCount:0}).decision,"allow");
});

test("Z-2 blocks command-local Git and PowerShell aliases that resolve to git stash",()=>{
  assert.equal(pre("Bash",{command:"git config alias.s stash; git s"}).rule,"Z-2");
  assert.equal(pre("Bash",{command:"git config alias.s 'stash -u'; git s"}).rule,"Z-2");
  assert.equal(pre("Bash",{command:"git config alias.s '!git stash'; git s"}).decision,"ask");
  assert.equal(pre("Bash",{command:"git -c alias.s=stash s"}).rule,"Z-2");
  assert.equal(pre("Bash",{command:"alias g='git'; g stash"}).rule,"Z-2");
  assert.equal(pre("PowerShell",{command:"Set-Alias g git; g stash"}).rule,"Z-2");
  assert.equal(pre("PowerShell",{command:"New-Alias -Name g -Value git; g stash"}).rule,"Z-2");
});
test("Z-2 asks before unresolved aliases or dynamic PowerShell command execution",()=>{
  assert.equal(pre("Bash",{command:"git s"}).decision,"ask");
  assert.equal(pre("Bash",{command:"git diff-tree --no-commit-id -r HEAD"}).decision,"allow");
  assert.equal(pre("Bash",{command:"git merge-base HEAD HEAD~1"}).decision,"allow");
  for(const command of ["g stash","g reset --hard HEAD","g push --force origin main","g add .","g commit -a -m x -- src/a.ts","g commit -m x","g config core.hooksPath .hooks"])assert.equal(pre("PowerShell",{command}).decision,"ask",command);
  assert.equal(pre("PowerShell",{command:"Invoke-Expression 'git stash'"}).decision,"ask");
  assert.equal(pre("PowerShell",{command:"Start-Process git -ArgumentList stash"}).rule,"Z-2");
  assert.equal(pre("PowerShell",{command:"Start-Process git -ArgumentList status"}).decision,"allow");
  assert.equal(pre("PowerShell",{command:"Start-Process -FilePath git.exe -ArgumentList 'reset --hard HEAD'"}).rule,"Z-3");
  assert.equal(pre("PowerShell",{command:"Start-Process -ArgumentList stash -FilePath git"}).rule,"Z-2");
  assert.equal(pre("PowerShell",{command:"& $env:GIT_CMD stash"}).decision,"ask");
});
