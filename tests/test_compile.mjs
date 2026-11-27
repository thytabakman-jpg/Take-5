import {digest,snapshot,decompile} from '../runtime/compile_decompiler.mjs';
import {dependency} from '../runtime/compile_dependencies.mjs';
import {verify} from '../runtime/compile_verify.mjs';
function tests(digest,snapshot,decompile,dependency,verify){
  let n=0;function check(ok,msg){if(!ok)throw Error("FAIL: "+msg);n++;}
  check(digest("")==="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","sha empty");
  check(digest("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","sha abc");
  const a="o/r:old/A.md",b="o/r:keep/B.md",c="o/r:index.md",x="o/other:README.md",z="o/r:source.md";
  const before={[a]:"# Original\n\nFacts.\n\n[Source](../source.md)\n",[b]:"# Retained\n\nFacts.\n",[c]:"[Old](old/A.md#original)\n",[x]:"[Old](https://github.com/o/r/blob/main/old/A.md#original)\n",[z]:"Evidence.\n"};
  const d=decompile({files:before,history:[{id:"old-revision",text:"Historical.\n"}]});
  check(d.units.filter(u=>u.source===a).map(u=>u.text).join("")===before[a],"lossless round trip");
  check(d.exactGroups.some(g=>g.length===2),"duplicates");
  check(!decompile({files:before,maxPairs:0}).comparisonComplete,"bounded pair comparisons");
  check(decompile({files:{[a]:"```md\n# not a heading\n```\n"}}).units[0].kind==="code","fenced code");
  const moves={[a]:b},anchors={[a+"#original"]:b+"#retained"};
  const prep=dependency({before,moves,anchors});
  check(prep.edits[c].includes("keep/B.md#retained"),"relative inbound link");
  check(prep.edits[x].includes("keep/B.md#retained"),"cross repo");
  check(dependency({before,moves}).issues.some(i=>i.kind==="ANCHOR_MAPPING_REQUIRED"),"missing anchor");
  const after={...before,[b]:"# Retained\n\nFacts.\n\n[Source](../source.md)\n",[c]:prep.edits[c],[x]:prep.edits[x]};delete after[a];
  const audit=dependency({before,after,moves,anchors,mode:"audit"});
  check(audit.status==="SUPPORTED_REFERENCES_VERIFIED",JSON.stringify(audit.issues));
  const wrong={...after,[c]:"[Wrong](keep/B.md#missing)\n"};
  check(dependency({before,after:wrong,moves,anchors,mode:"audit"}).status==="OPEN","wrong anchor");
  check(dependency({before,after:{...after,[z]:"`old/A.md`\n"},moves,anchors,mode:"audit"}).issues.some(i=>i.kind==="RETIRED_PATH_LITERAL_REVIEW"),"code path residual");
  const dispositions={};for(const u of d.units){if(u.kind==="separator"||after[u.source]===before[u.source]&&!u.historical)continue;const target=u.source===a?b:u.source;
    if(u.historical){dispositions[u.id]={kind:"historical",reference:"https://github.com/o/r/blob/"+"a".repeat(40)+"/old/A.md",reviewed:true,rationale:"Preserved historical witness"};continue;}
    const start=after[target].indexOf(u.text);dispositions[u.id]=start>=0?{kind:"exact",target,start,end:start+u.text.length}:{kind:"semantic",target,start:0,end:after[target].length,reviewed:true,rationale:"Reviewer accepted reformulation and reference mapping"};
  }
  const input={before,after,decomposition:d,dependencyReport:audit,dispositions,retire:[a],allowedChanges:[b,c,x],history:[{id:"old-revision",text:"Historical.\n"}],scopeReview:{complete:true,evidence:"Fixture scope and references reviewed."}};
  check(verify(input).status==="READY_FOR_PUBLICATION",JSON.stringify(verify(input).issues));
  check(verify({...input,dispositions:{}}).status==="OPEN","missing coverage");
  check(verify({...input,after:wrong}).status==="OPEN","stale audit");
  check(verify({...input,retire:[]}).issues.includes("UNAUTHORIZED_DELETION:"+a),"unauthorized deletion");
  check(verify({...input,allowedChanges:[]}).issues.includes("UNAUTHORIZED_EDIT:"+b),"unauthorized edit");
  check(verify({...input,publication:{revision:"a".repeat(40),baseDigest:snapshot(before),files:after}}).status==="PUBLISHED_SNAPSHOT_MATCHED","publication match");
  check(verify({...input,publication:{revision:"a".repeat(40),baseDigest:snapshot(before),files:wrong}}).status==="OPEN","publication mismatch");
  check(verify({...input,scopeReview:null}).status==="OPEN","scope gate");
  const tampered={...d,units:d.units.filter(u=>u.source!==a)};check(verify({...input,decomposition:tampered}).status==="OPEN","source coverage tampering");
  const scoped=decompile({files:before,targets:[a,b]});
  check(scoped.sources.length===2&&scoped.sourceDigest===snapshot(before),"target-only decomposition with full snapshot identity");
  const minimal={...input,decomposition:scoped,history:[],dispositions:Object.fromEntries(Object.entries(dispositions).filter(([k])=>scoped.units.some(u=>u.id===k&&u.kind==="heading"&&u.source===a)))};
  // The unique facts, unchanged survivor heading and unchanged source reference are matched automatically.
  const minResult=verify(minimal);
  check(minResult.status==="READY_FOR_PUBLICATION",JSON.stringify(minResult.issues));
  check(minResult.autoExact.length>=2&&minResult.mechanicalEdits.length===2,"automatic exact and mechanical edit receipts");
  const residualAfter={...after,[z]:"Evidence.\n\nHistorical mention of old/A.md.\n"};
  const residual=dependency({before,after:residualAfter,moves,anchors,mode:"audit"});
  const issue=residual.issues.find(i=>i.kind==="RETIRED_PATH_LITERAL_REVIEW");
  check(!!issue,"literal requires review");
  const literalReviews=[{source:issue.source,target:issue.target,contentDigest:issue.contentDigest,reviewed:true,rationale:"Historical mention, not an operative dependency."}];
  check(dependency({before,after:residualAfter,moves,anchors,literalReviews,mode:"audit"}).status==="SUPPORTED_REFERENCES_VERIFIED","reviewed benign literal");
  check(dependency({before,after:{...residualAfter,[z]:residualAfter[z]+"changed"},moves,anchors,literalReviews,mode:"audit"}).status==="OPEN","stale literal review");
  check(dependency({before,after:{...after,[z]:"[New](missing.md)\n"},moves,anchors,mode:"audit"}).issues.some(i=>i.kind==="NEW_UNRESOLVED_INTERNAL_TARGET"),"new unresolved internal reference");
  check(verify({...minimal,after:{...after,[z]:"Changed evidence."}}).issues.some(i=>i==="UNDECOMPOSED_CHANGED_SOURCE:"+z),"unreviewed collateral change");
  return n;
}
console.log(tests(digest,snapshot,decompile,dependency,verify)+' assertions passed');
