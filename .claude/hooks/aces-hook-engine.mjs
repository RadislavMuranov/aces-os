import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import crypto from "node:crypto";
import { validateDefectControlSet, validatePolicyControlSet } from "./aces-policy-controls.mjs";

export const REQUIRED_DEFECT_IDS = [
  ...Array.from({length:20},(_,i)=>"BUG-"+String(i+1).padStart(3,"0")),
  "B-129","B-135","B-136"
];
export const REQUIRED_POLICY_IDS = [
  "METHOD-SELECTION-001",
  ...Array.from({length:9},(_,i)=>"AGENTS-"+String(i+1).padStart(2,"0")),
  ...Array.from({length:24},(_,i)=>"SCHEMA-"+String(i+1).padStart(2,"0")),
  ...Array.from({length:19},(_,i)=>"FF-"+String(i+1).padStart(2,"0")),
  ...Array.from({length:20},(_,i)=>"SA-"+String(i+1).padStart(2,"0")),
  ..."ABCDEFGHIJKL".split("").map(x=>"SA-"+x),
  ...Array.from({length:15},(_,i)=>"BP-"+String(i+1).padStart(2,"0")),
  ...Array.from({length:12},(_,i)=>"BC-"+String(i+1).padStart(2,"0")),
  ...Array.from({length:8},(_,i)=>"Z-"+(i+1)),
  ...Array.from({length:19},(_,i)=>"ITR-"+String(i+1).padStart(2,"0")),
  ...Array.from({length:8},(_,i)=>"BC-I"+(i+1)),
  ...Array.from({length:8},(_,i)=>"KMA-"+String(i+1).padStart(2,"0"))
];
const PROTECTED = ["/agents.md","/schema.md","/spec/master-protocol.md",
  "/spec/governance/chatgpt-failure-filter.md",
  "/spec/governance/chatgpt-iteration-self-audit-rule.md",
  "/spec/governance/chatgpt-iteration-refactor-and-bug-learning-gate.md",
  "/spec/governance/chatgpt-bug-prevention-rules.md",
  "/spec/chatgpt-bug-control-spec.md","/docs/audit/kma-11-chatgpt-bug-system.md"];
const VERIFY = /\b(node\s+--test|npm\s+(?:run\s+)?test|npx\s+(?:vitest|jest)|vitest\s+run|jest\b|pytest\b|cargo\s+test|go\s+test|dotnet\s+test|mvn\s+test|gradle\s+test|tsc\s+--noEmit|npm\s+run\s+(?:build|typecheck|lint))\b/i;

const normPath = s => String(s||"").replace(/\\/g,"/").replace(/\/+/g,"/").toLowerCase();
function secretPath(s) {
  const p=normPath(s), b=p.split("/").pop()||"";
  return b!==".env.example" && /(?:^|[:/])\.env(?:\.[^/]+)?$/i.test(p);
}
function tokenize(src, shell, depth=0) {
  if(depth>8) return {segments:[],nested:[],error:true};
  const toks=[],nested=[]; let w="",started=false,q=null,error=false;
  const bt=String.fromCharCode(96);
  const push=()=>{if(started)toks.push({v:w,t:0});w="";started=false;};
  const op=x=>{push();toks.push({v:x,t:1});};
  const sub=body=>{const r=tokenize(body,shell,depth+1);nested.push(...r.nested,...r.segments);if(r.error)error=true;};
  const paren=(s,i)=>{let d=1,quote=null,esc=false;for(let j=i+2;j<s.length;j++){let c=s[j];if(esc){esc=false;continue;}if(quote){if(c==="\\"&&quote==='"'){esc=true;continue;}if(c===quote)quote=null;continue;}if(c==="'"||c==='"'){quote=c;continue;}if(c==="(")d++;if(c===")"&&--d===0)return {body:s.slice(i+2,j),end:j+1};}return null;};
  for(let i=0;i<src.length;i++){
    const c=src[i],n=src[i+1];
    if(q){
      if(q==='"'&&c==="$"&&n==="("){const x=paren(src,i);if(!x){error=true;break;}sub(x.body);w+=" __SUB__ ";i=x.end-1;continue;}
      if(shell==="bash"&&q==='"'&&c===bt){const e=src.indexOf(bt,i+1);if(e<0){error=true;break;}sub(src.slice(i+1,e));w+=" __SUB__ ";i=e;continue;}
      if(shell==="powershell"&&q==="'"&&c==="'"&&n==="'"){w+="'";i++;continue;}
      if(shell==="powershell"&&q==='"'&&c===bt&&n){w+=n;i++;continue;}
      if(shell==="bash"&&q==='"'&&c==="\\"&&n){w+=n;i++;continue;}
      if(c===q){q=null;continue;}w+=c;started=true;continue;
    }
    if(shell==="powershell"&&c==="<"&&n==="#"){const e=src.indexOf("#>",i+2);if(e<0){error=true;break;}i=e+1;continue;}
    if(/\s/.test(c)){push();if(c==="\n"||c==="\r")op("\n");continue;}
    if(c==="#"&&!started){while(i<src.length&&src[i]!=="\n")i++;i--;continue;}
    if(c==="'"||c==='"'){q=c;started=true;continue;}
    if(c==="$"&&n==="("){const x=paren(src,i);if(!x){error=true;break;}sub(x.body);w+=" __SUB__ ";started=true;i=x.end-1;continue;}
    if(shell==="bash"&&c===bt){const e=src.indexOf(bt,i+1);if(e<0){error=true;break;}sub(src.slice(i+1,e));w+=" __SUB__ ";started=true;i=e;continue;}
    if(shell==="bash"&&c==="\\"&&n){w+=n;started=true;i++;continue;}
    if((c==="&"||c==="|")&&n===c){op(c+c);i++;continue;}
    if(c===";"||c==="|"||(shell==="bash"&&c==="&")){op(c);continue;}
    if((c==="{"||c==="}")||(shell==="bash"&&(c==="("||c===")"))||(shell==="powershell"&&(c==="("||c===")"))){op(c);continue;}
    w+=c;started=true;
  }
  if(q)error=true;push();
  const seps=shell==="bash"?new Set([";","&&","||","|","&","\n","(",")","{","}"]):new Set([";","&&","||","|","\n","(",")","{","}"]);
  const segments=[];let cur=[];
  for(const t of toks){if(t.t===1&&seps.has(t.v)){if(cur.length)segments.push(cur);cur=[];}else cur.push(t);}
  if(cur.length)segments.push(cur);
  return {segments,nested,error};
}
const base=s=>String(s||"").replace(/\\/g,"/").split("/").pop().toLowerCase().replace(/\.exe$/,"");
function commandOf(words,shell) {
  let i=0;while(words[i]==="&")i++;
  while(["then","do","else","elif","fi","done"].includes(String(words[i]||"").toLowerCase()))i++;
  while(i<words.length&&/^[a-z_][a-z0-9_]*=.*/i.test(words[i]))i++;
  let cmd=base(words[i]),args=words.slice(i+1);
  if(["sudo","command","time","nohup","nice","exec"].includes(cmd))return commandOf(args,shell);
  if(cmd==="env"){let j=0;while(j<args.length&&(args[j].startsWith("-")||/^[a-z_][a-z0-9_]*=.*/i.test(args[j])))j++;return commandOf(args.slice(j),shell);}
  if(["bash","sh","zsh","pwsh","powershell"].includes(cmd)){let k=args.findIndex(x=>["-c","--command","-command"].includes(x.toLowerCase()));if(k>=0&&args[k+1])return {cmd,args,nested:args[k+1]};}
  if(cmd==="cmd"){let k=args.findIndex(x=>x.toLowerCase()==="/c");if(k>=0&&args[k+1])return {cmd,args,nested:args[k+1]};}
  return {cmd,args,nested:null};
}
function gitSub(args){
  let i=0;
  while(i<args.length){
    const x=args[i];
    if(["-c","-C","--git-dir","--work-tree","--namespace","--config-env"].includes(x)){
      const v=args[i+1]||"";
      if((x==="-c"||x==="--config-env")&&/^core\.hookspath=/i.test(v))return {rule:"Z-1",decision:"deny",reason:"Changing core.hooksPath is prohibited."};
      i+=2;continue;
    }
    if(x.startsWith("-c")&&/core\.hookspath=/i.test(x))return {rule:"Z-1",decision:"deny",reason:"Overriding core.hooksPath is prohibited."};
    if(x.startsWith("-")){i++;continue;}
    return {sub:x.toLowerCase(),args:args.slice(i+1)};
  }
  return {sub:"",args:[]};
}
const GIT_RECOGNIZED_SUBCOMMANDS = new Set("add am annotate apply archive bisect blame branch bundle cat-file check-attr check-ignore check-mailmap check-ref-format checkout cherry cherry-pick citool clean clone commit config count-objects credential credential-cache credential-store daemon describe diff diff-files diff-index diff-tree difftool fast-export fast-import fetch filter-branch for-each-ref format-patch fsck gc get-tar-commit-id grep gui help index-pack init instaweb log ls-files ls-remote ls-tree maintenance merge merge-base merge-file mergetool mv name-rev notes pack-objects pack-refs prune pull push range-diff rebase read-tree reflog remote repack replace request-pull reset restore rev-parse rev-list revert rm send-email shortlog show show-ref sparse-checkout stash status submodule switch symbolic-ref tag unpack-objects update-index update-ref verify-commit verify-tag version whatchanged worktree write-tree".split(" "));
function collectAliases(parsed,shell){
  const shellAliases=new Map(),gitAliases=new Map();
  for(const seg of [...parsed.nested,...parsed.segments]){
    const words=seg.filter(t=>t.t===0).map(t=>t.v);
    const {cmd,args}=commandOf(words,shell);
    if(shell==="powershell"&&["set-alias","new-alias","sal","nal"].includes(cmd)){
      const ni=args.findIndex(x=>x.toLowerCase()==="-name"),vi=args.findIndex(x=>x.toLowerCase()==="-value");
      const name=ni>=0?args[ni+1]:args[0],value=vi>=0?args[vi+1]:args[1];
      if(name&&base(value)==="git")shellAliases.set(name.toLowerCase(),"git");
    }
    if(shell==="bash"&&cmd==="alias"){
      for(const item of args){const m=String(item).match(/^([a-z0-9_-]+)=git$/i);if(m)shellAliases.set(m[1].toLowerCase(),"git");}
    }
    if(cmd==="git"){
      for(let i=0;i<args.length-1;i++){
        if(args[i]==="-c"){
          const m=String(args[i+1]).match(/^alias\.([a-z0-9_-]+)=(.*)$/i);
          if(m)gitAliases.set(m[1].toLowerCase(),m[2]);
        }
      }
      const g=gitSub(args);
      if(g.sub==="config"){
        const i=g.args.findIndex(x=>/^alias\.[a-z0-9_-]+$/i.test(x));
        if(i>=0&&g.args[i+1])gitAliases.set(g.args[i].slice(6).toLowerCase(),g.args[i+1]);
      }
    }
  }
  return {shellAliases,gitAliases};
}
function mayBeProtectedGit(args){
  const sub=String(args[0]||"").toLowerCase(),rest=args.slice(1);
  if(["stash","rebase"].includes(sub))return true;
  if(sub==="reset"&&rest.includes("--hard"))return true;
  if(sub==="push"&&rest.some(x=>["--force","-f","--force-with-lease"].includes(x)||x.startsWith("--force-with-lease=")||x.startsWith("+")))return true;
  if(sub==="add"&&rest.some(x=>["-A","--all","-u","--update",".","./"].includes(x)))return true;
  if(sub==="commit"){
    if(rest.some(x=>["--no-verify","-n","-a","--all"].includes(x)||/^-a[^-]/.test(x)))return true;
    const k=rest.indexOf("--");if(k<0||!rest.slice(k+1).some(x=>x.trim()))return true;
  }
  if(sub==="config"&&rest.some(x=>/^core\.hookspath(?:=|$)/i.test(x)||x==="--edit"))return true;
  return false;
}
function inspect(words,shell,depth=0,aliases={shellAliases:new Map(),gitAliases:new Map()}){
  if(depth>8)return {rule:"SHELL-PARSE-AMBIGUOUS",decision:"ask",reason:"Nested shell depth exceeded; inspect before execution."};
  if(shell==="powershell"&&words[0]==="&"&&String(words[1]||"").includes("$"))return {rule:"SHELL-PARSE-AMBIGUOUS",decision:"ask",reason:"Dynamic PowerShell command invocation; inspect the resolved executable before execution."};
  const first=String(words[0]||"").toLowerCase();
  if(aliases.shellAliases.has(first))words=["git",...words.slice(1)];
  const {cmd,args,nested}=commandOf(words,shell);if(!cmd)return null;
  if(shell==="powershell"&&["invoke-expression","iex"].includes(cmd))return {rule:"SHELL-PARSE-AMBIGUOUS",decision:"ask",reason:"Dynamic PowerShell expression; inspect the expanded command before execution."};
  if(shell==="powershell"&&["start-process","start"].includes(cmd)&&args.some(x=>base(x)==="git")){
    const ai=args.findIndex(x=>x.toLowerCase()==="-argumentlist");
    const stopParams=new Set(["-filepath","-workingdirectory","-verb","-windowstyle","-wait","-passthru","-nonewwindow","-loaduserprofile","-redirectstandardoutput","-redirectstandarderror","-redirectstandardinput","-usenewenvironment"]);
    const rest=ai>=0?args.slice(ai+1):args.slice(args.findIndex(x=>base(x)==="git")+1);
    const stop=rest.findIndex(x=>stopParams.has(x.toLowerCase()));
    const launchArgs=(stop>=0?rest.slice(0,stop):rest).flatMap(x=>String(x).split(/\s+/)).filter(Boolean);
    const result=inspect(["git",...launchArgs],"bash",depth+1,aliases);
    if(result)return result;
  }
  if(cmd!=="git"&&mayBeProtectedGit(args))return {rule:"SHELL-PARSE-AMBIGUOUS",decision:"ask",reason:"Unresolved command alias may invoke a protected Git operation; inspect its definition before execution."};
  if(nested){const ns=cmd==="pwsh"||cmd==="powershell"?"powershell":"bash";const p=tokenize(nested,ns,depth+1);if(p.error)return {rule:"SHELL-PARSE-AMBIGUOUS",decision:"ask",reason:"Nested shell syntax is ambiguous."};const nestedAliases=collectAliases(p,ns);for(const s of [...p.nested,...p.segments]){const r=inspect(s.filter(t=>t.t===0).map(t=>t.v),ns,depth+1,nestedAliases);if(r)return r;}if(/[$`]|__SUB__/.test(nested))return {rule:"SHELL-PARSE-AMBIGUOUS",decision:"ask",reason:"Dynamic nested shell command; inspect the expanded command before execution."};}
  const joined=words.join(" ");
  const researchPath=/(?:^|[\\/])(?:research|experiments|negative-results|benchmarks)(?:[\\/]|$)/i.test(joined);
  const deleteCommand=["rm","rmdir","del","erase","remove-item","rd"].includes(cmd)||(cmd==="git"&&gitSub(args).sub==="rm");
  if(researchPath&&deleteCommand)return {rule:"BUG-001/BUG-020",decision:"ask",reason:"Research/experiment/negative-result deletion requires a before/after inventory and explicit preservation verification."};
  const env=words.some(secretPath);
  if(env&&!["echo","printf","write-output","write-host"].includes(cmd)){
    if(cmd!=="git"||!["status","ls-files","check-ignore","rev-parse"].includes(gitSub(words.slice(1)).sub))
      return {rule:"Z-8",decision:"deny",reason:"Reading .env and .env.* is prohibited; .env.example is allowed."};
  }
  if(["python","python3","node","ruby","perl","php","pwsh","powershell"].includes(cmd)&&/\.env(?:\.[a-z0-9_-]+)?/i.test(words.join(" "))&&/\b(open\s*\(|readFile(?:Sync)?\s*\(|read_text\s*\(|get-content|readalltext)\b/i.test(words.join(" ")))
    return {rule:"Z-8",decision:"deny",reason:"Reading .env and .env.* is prohibited; .env.example is allowed."};
  if(cmd!=="git")return null;
  const g=gitSub(args);if(g.rule)return g;const a=g.args,s=g.sub;
  if(aliases.gitAliases.has(s)){
    const value=String(aliases.gitAliases.get(s)||"");
    if(value.startsWith("!"))return {rule:"SHELL-PARSE-AMBIGUOUS",decision:"ask",reason:"Git shell alias requires inspection before execution."};
    const p=tokenize(value,"bash",depth+1);
    if(p.error)return {rule:"SHELL-PARSE-AMBIGUOUS",decision:"ask",reason:"Git alias expansion is ambiguous."};
    for(const seg of [...p.nested,...p.segments]){const r=inspect(["git",...seg.filter(t=>t.t===0).map(t=>t.v)],"bash",depth+1,aliases);if(r)return r;}
    return null;
  }
  if(!GIT_RECOGNIZED_SUBCOMMANDS.has(s))return {rule:"SHELL-PARSE-AMBIGUOUS",decision:"ask",reason:"Unknown Git subcommand may be a configured alias; inspect it before execution."};
  if(s==="stash")return {rule:"Z-2",decision:"deny",reason:"All git stash operations are prohibited."};
  if(s==="reset"&&a.includes("--hard"))return {rule:"Z-3",decision:"deny",reason:"git reset --hard is prohibited."};
  if(s==="rebase")return {rule:"Z-4",decision:"deny",reason:"git rebase is prohibited."};
  if(s==="push"&&a.some(x=>["--force","-f","--force-with-lease"].includes(x)||x.startsWith("--force-with-lease=")||x.startsWith("+")))return {rule:"Z-5",decision:"deny",reason:"Force push and '+' refspecs are prohibited."};
  if(s==="add"&&a.some(x=>["-A","--all","-u","--update",".","./"].includes(x)))return {rule:"Z-6",decision:"deny",reason:"Broad git add operations are prohibited."};
  if(s==="commit"){
    if(a.some(x=>x==="--no-verify"||x==="-n"))return {rule:"Z-1",decision:"deny",reason:"Bypassing commit hooks is prohibited."};
    if(a.some(x=>x==="-a"||x==="--all"||/^-a[^-]/.test(x)))return {rule:"Z-7",decision:"deny",reason:"git commit -a is prohibited."};
    const k=a.indexOf("--");if(k<0||!a.slice(k+1).some(x=>x.trim()))return {rule:"Z-7",decision:"deny",reason:"git commit requires explicit paths after '--'."};
  }
  if(s==="config"){
    const k=a.findIndex(x=>/^core\.hookspath(?:=|$)/i.test(x));
    const read=a.some(x=>["--get","--get-all","--get-regexp","--list","-l"].includes(x));
    if(k>=0&&!read&&(a.includes("--unset")||a.includes("--unset-all")||a.length>k+1))return {rule:"Z-1",decision:"deny",reason:"Changing core.hooksPath is prohibited; reading it is allowed."};
    if(a.includes("--edit"))return {rule:"Z-1",decision:"ask",reason:"git config --edit may change core.hooksPath; confirm first."};
  }
  return null;
}

export function formatJournalRow(ts,rule,decision){return [ts,rule,decision].join("\t")+"\n";}
export function evaluatePreToolUse(input,state={verificationAttempts:{}}){
  const name=String(input?.tool_name||""),ti=input?.tool_input||{};
  if(["Read","Write","Edit"].includes(name)){
    const p=ti.file_path||"";
    if(secretPath(p))return {rule:"Z-8",decision:"deny",reason:"Access to .env and .env.* is prohibited; .env.example is allowed."};
    if(["Write","Edit"].includes(name)&&PROTECTED.some(x=>normPath(p).endsWith(x)))return {rule:"ACES-CANON-001",decision:"ask",reason:"Protected ACES governance file. Require explicit authorization and Master Control Protocol."};
    if(name==="Write"&&normPath(p).includes("/spec/governance/"))return {rule:"BUG-014",decision:"ask",reason:"New governance rules require an observed failure, existing-control analysis, and minimality justification before creation."};
    return {rule:"NO_MATCH",decision:"allow"};
  }
  if(name!=="Bash"&&name!=="PowerShell")return {rule:"NO_MATCH",decision:"allow"};
  const command=ti.command;if(typeof command!=="string"||!command.trim())return {rule:"NO_MATCH",decision:"allow"};
  const shell=name==="PowerShell"?"powershell":"bash",p=tokenize(command,shell);
  if(p.error)return {rule:"SHELL-PARSE-AMBIGUOUS",decision:"ask",reason:"Shell syntax is ambiguous or incomplete; inspect before execution."};
  const aliases=collectAliases(p,shell);
  for(const seg of [...p.nested,...p.segments]){const r=inspect(seg.filter(t=>t.t===0).map(t=>t.v),shell,0,aliases);if(r)return r;}
  for(const seg of p.segments){
    const words=seg.filter(t=>t.t===0).map(t=>t.v),n=words.join(" ").replace(/\s+/g," ").trim().toLowerCase();
    if(VERIFY.test(n)){
      const key=crypto.createHash("sha256").update(n).digest("hex"),a=state.verificationAttempts||(state.verificationAttempts={}),count=Number(a[key]||0);
      if(count>=2)return {rule:"BUDGET-RETRY-2",decision:"deny",reason:"This exact verification command has already been attempted twice in this session. Stop and report the blocker."};
      a[key]=count+1;
    }
  }
  return {rule:"NO_MATCH",decision:"allow"};
}
function parseRecord(message){
  const m=String(message||"").match(/<!--\s*ACES_ITERATION_RECORD([\s\S]*?)-->/i);if(!m)return null;
  const fields={},bugs={},defectControls={};
  for(const line of m[1].split(/\r?\n/)){const x=line.match(/^\s*(CONTROL (?:BUG-\d{3}|B-\d{3})|BUG-\d{3}|B-\d{3}|[A-Z][A-Z0-9 _-]*)\s*:\s*(.*?)\s*$/i);if(!x)continue;const k=x[1].trim().toUpperCase();if(/^CONTROL (?:BUG-\d{3}|B-\d{3})$/.test(k))defectControls[k.slice(8)]=x[2].trim();else if(/^(BUG-\d{3}|B-\d{3})$/.test(k))bugs[k]=x[2].trim().toUpperCase();else fields[k]=x[2].trim();}
  return {fields,bugs,defectControls};
}
const terminal=m=>/\b(?:VERDICT|ITERATION VERDICT|STATUS)\s*:\s*(?:PASS|FAIL|BLOCKED|STOP|CONDITIONAL)\b/i.test(String(m||""));
export function evaluateStop(input,state={turnCount:0}){
  const msg=String(input?.last_assistant_message||""),cwd=normPath(input?.cwd||process.env.CLAUDE_PROJECT_DIR||"");
  if(!/(?:^|\/)aces-os(?:\/|$)/i.test(cwd))return {rule:"STOP-GATE",decision:"allow"};
  state.turnCount=Number(state.turnCount||0)+1;
  if(state.turnCount>=40&&!terminal(msg))return {rule:"BUDGET-TURN-40",decision:"block",reason:"40-turn budget exhausted. Produce a terminal PASS/FAIL/BLOCKED/STOP disposition and exact blocker."};
  if(!/\b(?:VERDICT|ITERATION VERDICT|STATUS)\s*:\s*PASS\b/i.test(msg))return {rule:"STOP-GATE",decision:"allow"};
  const rec=parseRecord(msg);if(!rec)return {rule:"STOP-RECORD",decision:"block",reason:"PASS requires an ACES_ITERATION_RECORD with evidence and defect classifications."};
  const required=["TASK","REPOSITORY BEFORE","PRIMARY SOURCE","INSPECTION SCOPE","EVIDENCE CLASSIFICATION","NEGATIVE EVIDENCE","CONTRADICTIONS","MINIMALITY","VERIFICATION COMMAND","RAW OUTPUT","EXIT CODE","BUG AUDIT","REMAINING UNKNOWNS","REGRESSION CHECK","REPOSITORY AFTER","POLICY RULES CHECKED","VERDICT","NEXT ACTION"];
  const missing=required.filter(k=>!rec.fields[k]);
  if(rec.fields["EXIT CODE"]!=="0")missing.push("EXIT CODE: 0");
  if(rec.fields["BUG AUDIT"]!=="COMPLETE")missing.push("BUG AUDIT: COMPLETE");
  for(const id of REQUIRED_DEFECT_IDS){const s=rec.bugs[id];if(!s)missing.push(id);else if(!["CLEAR","N/A"].includes(s))missing.push(id+" classification must be CLEAR or N/A");}
  const defectControlErrors=validateDefectControlSet(REQUIRED_DEFECT_IDS,rec.defectControls);
  for(const e of defectControlErrors)missing.push("CONTROL "+e.id+": "+e.errors.join("|"));
  const policyMap=new Map(String(rec.fields["POLICY RULES CHECKED"]||"").split(/[;,]/).map(x=>x.trim().match(/^([A-Z0-9-]+)=(.+)$/i)).filter(Boolean).map(x=>[x[1],x[2]]));
  const policyControlErrors=validatePolicyControlSet(REQUIRED_POLICY_IDS,Object.fromEntries(policyMap),rec.fields,input?.cwd||process.env.CLAUDE_PROJECT_DIR||process.cwd());
  for(const e of policyControlErrors)missing.push("POLICY "+e.id+": "+e.errors.join("|"));
  if(!policyMap.has("METHOD-SELECTION-001"))missing.push("METHOD-SELECTION-001 method-selection evidence");
  if(/\b(not found|absent|does not exist|no .* found)\b/i.test(msg)&&rec.bugs["B-135"]==="N/A")missing.push("B-135 absence reconstruction");
  if(/\b(zero[- ]state|delete(?:d|ion)? research|research erasure)\b/i.test(msg)&&["N/A",undefined].includes(rec.bugs["B-129"]))missing.push("B-129 research preservation");
  return missing.length?{rule:"STOP-RECORD",decision:"block",reason:"PASS blocked; complete: "+[...new Set(missing)].join(", ")}:{rule:"STOP-RECORD",decision:"allow"};
}
export function statePath(project,session){const key=crypto.createHash("sha256").update(normPath(project)+"|"+String(session||"no-session")).digest("hex");return path.join(os.tmpdir(),"aces-claude-hook-state",key+".json");}
export function loadState(p){if(!fs.existsSync(p))return {turnCount:0,verificationAttempts:{}};const x=JSON.parse(fs.readFileSync(p,"utf8"));if(!x||typeof x!=="object")throw new Error("Invalid hook state");return {turnCount:Number(x.turnCount||0),verificationAttempts:x.verificationAttempts||{}};}
export function saveState(p,s){fs.mkdirSync(path.dirname(p),{recursive:true});const t=p+".tmp";fs.writeFileSync(t,JSON.stringify(s),"utf8");fs.renameSync(t,p);}
export function appendJournal(project,rule,decision){const p=path.join(project,".claude","hooks","journal.tsv");fs.mkdirSync(path.dirname(p),{recursive:true});if(!fs.existsSync(p))fs.writeFileSync(p,"timestamp\trule_id\tdecision\n","utf8");fs.appendFileSync(p,formatJournalRow(new Date().toISOString(),rule,decision),"utf8");}
async function run(){
  const mode=process.argv[2],input=JSON.parse(fs.readFileSync(0,"utf8")),project=input.cwd||process.env.CLAUDE_PROJECT_DIR||process.cwd(),p=statePath(project,input.session_id),state=loadState(p);
  if(mode==="pretool"){const r=evaluatePreToolUse(input,state);saveState(p,state);appendJournal(project,r.rule,r.decision);if(["deny","ask"].includes(r.decision))process.stdout.write(JSON.stringify({hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:r.decision,permissionDecisionReason:r.reason}}));return;}
  if(mode==="stop"){const r=evaluateStop(input,state);saveState(p,state);appendJournal(project,r.rule,r.decision);if(r.decision==="block")process.stdout.write(JSON.stringify({decision:"block",reason:r.reason}));return;}
  throw new Error("Unknown hook mode");
}
if(process.argv[2]==="pretool"||process.argv[2]==="stop")run().catch(e=>{process.stderr.write("ACES hook failed closed: "+String(e.message||e));process.exit(2);});
