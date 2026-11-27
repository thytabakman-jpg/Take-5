#!/usr/bin/env node
// Standalone Compile operator. Node 18+; no third-party packages.
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
function digest(s) {
  // SHA-256 of UTF-8, implemented once and embedded identically in each standalone tool.
  const bytes=Array.from(unescape(encodeURIComponent(s)),c=>c.charCodeAt(0));
  const bitLen=bytes.length*8; bytes.push(128); while(bytes.length%64!==56)bytes.push(0);
  const hi=Math.floor(bitLen/4294967296),lo=bitLen>>>0;
  for(const v of [hi,lo])for(let n=24;n>=0;n-=8)bytes.push((v>>>n)&255);
  const H=[],K=[];for(let p=2;K.length<64;p++){let prime=true;for(let q=2;q*q<=p;q++)if(p%q===0){prime=false;break;}if(!prime)continue;if(H.length<8)H.push((Math.sqrt(p)%1*4294967296)>>>0);K.push((Math.cbrt(p)%1*4294967296)>>>0);}
  const r=(x,n)=>(x>>>n)|(x<<(32-n));
  for(let off=0;off<bytes.length;off+=64){
    const w=[];for(let i=0;i<16;i++)w[i]=(bytes[off+4*i]<<24)|(bytes[off+4*i+1]<<16)|(bytes[off+4*i+2]<<8)|bytes[off+4*i+3];
    for(let i=16;i<64;i++){let a=w[i-15],b=w[i-2];w[i]=(w[i-16]+(r(a,7)^r(a,18)^(a>>>3))+w[i-7]+(r(b,17)^r(b,19)^(b>>>10)))|0;}
    let [a,b,c,d,e,f,g,h]=H;for(let i=0;i<64;i++){let t1=(h+(r(e,6)^r(e,11)^r(e,25))+((e&f)^(~e&g))+K[i]+w[i])|0,t2=((r(a,2)^r(a,13)^r(a,22))+((a&b)^(a&c)^(b&c)))|0;h=g;g=f;f=e;e=(d+t1)|0;d=c;c=b;b=a;a=(t1+t2)|0;}[a,b,c,d,e,f,g,h].forEach((v,i)=>H[i]=(H[i]+v)>>>0);
  }return H.map(v=>v.toString(16).padStart(8,"0")).join("");
}
function snapshot(files) {
  if(!files||typeof files!=="object"||Array.isArray(files))throw Error("files must be an object");
  const entries=Object.entries(files).sort(([a],[b])=>a<b?-1:a>b?1:0);
  for(const [id,value] of entries)if(typeof value!=="string"||!/^[^/:]+\/[^/:]+:[^#]+$/.test(id)||id.split(":")[1].split("/").some(p=>!p||p==="."||p===".."))throw Error("Invalid file ID or text: "+id);
  return digest(JSON.stringify(entries));
}
function verify(input){
  const {before,after,decomposition,dependencyReport,dispositions={},retire=[],allowedChanges=[],scopeReview,publication}=input;
  const beforeDigest=snapshot(before),afterDigest=snapshot(after),issues=[],semantic=[],autoExact=[],mechanicalEdits=[];
  if(!decomposition||decomposition.sourceDigest!==beforeDigest)issues.push("DECOMPOSITION_STALE_OR_MISSING");
  if(!dependencyReport||dependencyReport.mode!=="audit"||dependencyReport.beforeDigest!==beforeDigest||dependencyReport.afterDigest!==afterDigest||dependencyReport.status!=="SUPPORTED_REFERENCES_VERIFIED"||dependencyReport.issues?.length!==0)issues.push("DEPENDENCY_AUDIT_OPEN_OR_STALE");
  if(!scopeReview||scopeReview.complete!==true||typeof scopeReview.evidence!=="string"||!scopeReview.evidence.trim())issues.push("SCOPE_AND_UNSUPPORTED_DEPENDENCIES_REVIEW_REQUIRED");
  const units=decomposition?.units||[],sources=decomposition?.sources||[],ids=new Set(),retired=new Set(retire),allowed=new Set(allowedChanges);
  const historical=Object.fromEntries((input.history||[]).map(h=>[h.id,h.text]));
  for(const source of sources){const text=source.historical?historical[source.source]:before[source.source];if(typeof text!=="string"||digest(text)!==source.digest){issues.push("SOURCE_MISMATCH:"+source.source);continue;}let pos=0;for(const u of units.filter(u=>u.source===source.source&&u.historical===source.historical).sort((a,b)=>a.start-b.start)){if(u.start!==pos||u.end<=u.start||text.slice(u.start,u.end)!==u.text||u.id!==digest(JSON.stringify([u.source,u.start,u.end,u.historical])))issues.push("INVALID_SOURCE_SPAN:"+u.id);pos=u.end;}if(pos!==text.length)issues.push("INCOMPLETE_SOURCE_COVERAGE:"+source.source);}
  for(const id of Object.keys(before))if(before[id]!==after[id]&&!sources.some(s=>s.source===id&&!s.historical)){if(!retired.has(id)&&typeof after[id]==="string"&&dependencyReport?.edits?.[id]===after[id])mechanicalEdits.push(id);else issues.push("UNDECOMPOSED_CHANGED_SOURCE:"+id);}
  for(const id of decomposition?.targets||[])if(!sources.some(s=>s.source===id&&!s.historical))issues.push("UNDECOMPOSED_SELECTED_SOURCE:"+id);
  for(const id of Object.keys(historical))if(!sources.some(s=>s.source===id&&s.historical))issues.push("UNDECOMPOSED_HISTORY:"+id);
  let exact=0,reviewed=0;
  for(const u of units){
    if(ids.has(u.id)){issues.push("DUPLICATE_UNIT_ID:"+u.id);continue;}ids.add(u.id);
    if(!sources.some(s=>s.source===u.source&&s.historical===u.historical)){issues.push("UNKNOWN_SOURCE:"+u.id);continue;}
    // Structural separators are reproducible formatting, not protected semantic content.
    if(u.kind==="separator"&&!u.text.trim())continue;
    if(!u.historical&&after[u.source]===before[u.source]){exact++;continue;}
    let d=dispositions[u.id];
    if(!d&&!u.historical){const target=retired.has(u.source)?dependencyReport?.moves?.[u.source]:u.source;const text=after[target];if(typeof text==="string"){const start=text.indexOf(u.text);if(start>=0&&text.indexOf(u.text,start+1)<0){d={kind:"exact",target,start,end:start+u.text.length};autoExact.push({unit:u.id,...d});}}}
    if(!d){issues.push("MISSING_DISPOSITION:"+u.id);continue;}
    if(d.kind==="exact"||d.kind==="semantic"){
      const target=after[d.target];if(typeof target!=="string"||!Number.isInteger(d.start)||!Number.isInteger(d.end)||d.start<0||d.end<=d.start||d.end>target.length){issues.push("INVALID_TARGET_SPAN:"+u.id);continue;}
      const span=target.slice(d.start,d.end);
      if(d.kind==="exact"){if(span!==u.text)issues.push("EXACT_MISMATCH:"+u.id);else exact++;}
      else if(typeof d.rationale==="string"&&d.rationale.trim()&&d.reviewed===true){reviewed++;semantic.push(u.id);}else issues.push("SEMANTIC_REVIEW_REQUIRED:"+u.id);
    }else if(d.kind==="authorized-removal"&&d.reviewed===true&&typeof d.authorization==="string"&&d.authorization.trim()&&typeof d.rationale==="string"&&d.rationale.trim()){reviewed++;semantic.push(u.id);}
    else if(d.kind==="historical"&&u.historical&&d.reviewed===true&&typeof d.reference==="string"&&/^https:\/\/github\.com\/[^/]+\/[^/]+\/blob\/[0-9a-f]{40}\//i.test(d.reference)&&typeof d.rationale==="string"&&d.rationale.trim()){reviewed++;semantic.push(u.id);}
    else issues.push("UNSUPPORTED_DISPOSITION:"+u.id);
  }
  for(const id of Object.keys(before))if(!(id in after)){if(!retired.has(id))issues.push("UNAUTHORIZED_DELETION:"+id);}else if(before[id]!==after[id]&&!allowed.has(id))issues.push("UNAUTHORIZED_EDIT:"+id);
  for(const id of Object.keys(after))if(!(id in before)&&!allowed.has(id))issues.push("UNAUTHORIZED_CREATION:"+id);
  for(const id of retired){if(!(id in before)||id in after)issues.push("RETIREMENT_NOT_REALIZED:"+id);}
  let status=issues.length?"OPEN":"READY_FOR_PUBLICATION";
  if(publication){if(typeof publication.revision!=="string"||!(/^[0-9a-f]{40}$/i.test(publication.revision))||publication.baseDigest!==beforeDigest||snapshot(publication.files)!==afterDigest)issues.push("PUBLICATION_MISMATCH");status=issues.length?"OPEN":"PUBLISHED_SNAPSHOT_MATCHED";}
  return {status,beforeDigest,afterDigest,issues,exact,reviewed,semantic,autoExact,mechanicalEdits,limitations:["Semantic decisions and scope/functional evidence are supplied by the reviewer, not proven by this tool.","Published snapshot identity must be independently retrieved from the repository."]};
}
export { digest, snapshot, verify };
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try { console.log(JSON.stringify(verify(JSON.parse(readFileSync(0, 'utf8'))),null,2)); }
  catch (error) { console.error(error.message); process.exitCode=1; }
}
