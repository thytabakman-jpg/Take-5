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
function inventory(input){
  const {before,after,moves={},specs=[]}=input;
  const beforeDigest=snapshot(before);if(after)snapshot(after);
  const edits={},receipts=[],issues=[],seenSources=new Set();
  for(const spec of specs){
    const {source,entriesKey="entries",pathKey="path",countKey="count"}=spec;
    if(typeof before[source]!=="string"||typeof entriesKey!=="string"||typeof pathKey!=="string"||typeof countKey!=="string"||entriesKey===countKey)throw Error("Invalid inventory spec");
    if(seenSources.has(source))throw Error("Duplicate inventory source");seenSources.add(source);
    let doc;try{doc=JSON.parse(before[source]);}catch{issues.push({kind:"UNSUPPORTED_INVENTORY",source});continue;}
    if(!doc||!Array.isArray(doc[entriesKey])||!Number.isInteger(doc[countKey])||doc[countKey]!==doc[entriesKey].length||doc[entriesKey].some(x=>!x||typeof x!=="object"||Array.isArray(x)||typeof x[pathKey]!=="string"||!Object.hasOwn(before,x[pathKey]))){issues.push({kind:"UNSUPPORTED_OR_STALE_INVENTORY",source});continue;}
    const rows=[],seen=new Set();let removed=0;
    const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
    for(const row of doc[entriesKey]){const target=Object.hasOwn(moves,row[pathKey])?moves[row[pathKey]]:row[pathKey];const next={...row,[pathKey]:target},key=JSON.stringify(canonical(next));if(seen.has(key)){removed++;continue;}seen.add(key);rows.push(next);}
    const text=JSON.stringify({...doc,[entriesKey]:rows,[countKey]:rows.length},null,2)+"\n";
    edits[source]=text;receipts.push({source,entriesKey,pathKey,countKey,beforeCount:doc[countKey],afterCount:rows.length,removed,contentDigest:digest(text)});
    if(after){if(after[source]!==text)issues.push({kind:"INVENTORY_OUTPUT_MISMATCH",source});for(const row of rows)if(!Object.hasOwn(after,row[pathKey]))issues.push({kind:"INVENTORY_TARGET_MISSING",source,target:row[pathKey]});}
  }return {mode:"inventory",beforeDigest,afterDigest:after?snapshot(after):null,moves,edits,receipts,issues,status:issues.length?"OPEN":after?"INVENTORY_VERIFIED":"INVENTORY_PREPARED"};
}
function dependency(input){
  if(input.mode==='inventory')return inventory(input);
  const {before,after=before,moves={},anchors={},mode="prepare",literalReviews=[],relationshipReviews=[],referenceIndex,roots=[],includeIndex=false}=input;
  const beforeDigest=snapshot(before),afterDigest=snapshot(after);
  if(!["prepare","audit","index"].includes(mode))throw Error("Unknown mode");
  const issues=[],edits={},ledger=[],unchecked=[],reviewedResiduals=[],reviewedRelationships=[],indexStats={parsed:0,reused:0};
  const own=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);
  const split=id=>{const i=id.indexOf(":");return [id.slice(0,i),id.slice(i+1)];};
  const dirname=p=>p.includes("/")?p.slice(0,p.lastIndexOf("/")):"";
  const dec=s=>{try{return decodeURIComponent(s);}catch{return null;}};
  const enc=s=>s.split("/").map(encodeURIComponent).join("/");
  const norm=p=>{const out=[];for(const part of p.split("/")){if(!part||part===".")continue;if(part===".."){if(!out.length)return null;out.pop();}else out.push(part);}return out.join("/");};
  const rel=(from,to)=>{const a=dirname(from).split("/").filter(Boolean),b=to.split("/");while(a.length&&b.length&&a[0]===b[0]){a.shift();b.shift();}return [...a.map(()=>".."),...b].join("/")||".";};
  const dest=id=>own(moves,id)?moves[id]:id;
  const validId=id=>typeof id==="string"&&/^[^/:]+\/[^/:]+:[^#]+$/.test(id)&&split(id)[1].split("/").every(p=>p&&p!=="."&&p!=="..");
  for(const [a,b] of Object.entries(moves)){if(!own(before,a)||!validId(b)||a===b||own(moves,b))throw Error("Invalid or chained move: "+a);}
  for(const [a,b] of Object.entries(anchors)){if(!a.includes("#")||!b.includes("#")||!own(before,a.split("#")[0])||!validId(b.split("#")[0])||own(moves,b.split("#")[0]))throw Error("Invalid anchor mapping: "+a);}
  const retired=Object.keys(moves);
  function parse(raw,source){
    const [repo,path]=split(source);
    if(/^https?:\/\/github\.com\//i.test(raw)){
      const m=raw.match(/^https?:\/\/github\.com\/([^/]+\/[^/]+)\/(?:blob|tree)\/main\/([^?#]+)(?:#(.*))?$/i);
      if(!m)return null;let p=dec(m[2]),a=dec(m[3]||"");return p===null||a===null?null:{id:m[1]+":"+p,anchor:a,style:"github"};
    }
    if(/^(?:[a-z][a-z\d+.-]*:|\/\/)/i.test(raw))return null;
    const m=raw.match(/^([^?#]*)(?:#(.*))?$/);if(!m)return null;
    const p=dec(m[1]),a=dec(m[2]||"");if(p===null||a===null)return null;
    const target=p?norm((p.startsWith("/")?"":dirname(path)+"/")+p):path;
    return target===null?null:{id:repo+":"+target,anchor:a,style:p.startsWith("/")?"root":"relative"};
  }
  function refs(text){
    const result=[];let offset=0,fence=null,inComment=false;
    for(const line of text.match(/[^\n]*\n|[^\n]+$/g)||[]){
      const fm=line.match(/^ {0,3}(`{3,}|~{3,})/);
      if(fm){if(!fence)fence=fm[1];else if(fm[1][0]===fence[0]&&fm[1].length>=fence.length)fence=null;offset+=line.length;continue;}
      if(fence){offset+=line.length;continue;}
      const masked=line.replace(/`+[^`\n]*`+/g,m=>" ".repeat(m.length));
      const patterns=[/!?\[[^\]\n]+\]\(\s*(?:<([^>\n]+)>|([^\s()]+))/g,/^\s*\[[^\]\n]+\]:\s*(?:<([^>\n]+)>|([^\s]+))/g,/\b(?:href|src)\s*=\s*["']([^"']+)["']/gi, /https?:\/\/github\.com\/[^\s<>"'`)\]]+/gi];
      const occupied=[];
      for(let pi=0;pi<patterns.length;pi++)for(const m of masked.matchAll(patterns[pi])){
        const raw=pi===3?m[0]:(m[1]??m[2]);if(!raw)continue;
        const start=m.index+(pi===3?0:m[0].lastIndexOf(raw)),end=start+raw.length;
        if(occupied.some(([a,b])=>start<b&&end>a))continue;
        const lead=masked.slice(0,start);if(inComment||lead.lastIndexOf("<!--")>lead.lastIndexOf("-->"))continue;
        if(pi===0&&!masked.slice(end).match(/^>?(?:[ \t]+["'][^"']*["'])?[ \t]*\)/))continue;
        occupied.push([start,end]);result.push({start:offset+start,end:offset+end,raw,kind:["markdown-inline","markdown-definition","html-attribute","github-url"][pi]});
      }
      if(line.includes("<!--")||line.includes("-->"))inComment=line.lastIndexOf("<!--")>line.lastIndexOf("-->");
      offset+=line.length;
    }return result.sort((a,b)=>a.start-b.start);
  }
  function availableAnchors(text){
    const set=new Set(),seen=new Map();let fence=null;
    for(const line of text.split("\n")){
      const fm=line.match(/^ {0,3}(`{3,}|~{3,})/);if(fm){if(!fence)fence=fm[1];else if(fm[1][0]===fence[0]&&fm[1].length>=fence.length)fence=null;continue;}if(fence)continue;
      for(const m of line.matchAll(/<(?:a|[a-z][a-z\d-]*)\b[^>]*\b(?:id|name)=["']([^"']+)["']/gi))set.add(m[1]);
      const h=line.match(/^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$/);if(!h)continue;
      let base=h[1].toLowerCase().replace(/<[^>]+>/g,"").replace(/[^\p{L}\p{N}\p{M}_ -]/gu,"").replace(/ /g,"-");let n=seen.get(base)||0,slug=n?base+"-"+n:base;while(set.has(slug)){n++;slug=base+"-"+n;}seen.set(base,n+1);set.add(slug);
    }return set;
  }
  function transform(p){
    const key=p.id+(p.anchor?"#"+p.anchor:"");
    if(own(anchors,key)){const a=anchors[key],i=a.indexOf("#");return {id:a.slice(0,i),anchor:a.slice(i+1)};}
    if(p.anchor&&own(moves,p.id)){issues.push({kind:"ANCHOR_MAPPING_REQUIRED",target:key});return null;}
    return {id:dest(p.id),anchor:p.anchor};
  }
  function format(p,t,source){
    const [r,s]=split(source),[tr,tp]=split(t.id);const frag=t.anchor?"#"+encodeURIComponent(t.anchor):"";
    if(p.style==="github"||r!==tr)return "https://github.com/"+tr+"/blob/main/"+enc(tp)+frag;
    if(p.style==="root")return "/"+enc(tp)+frag;
    if(source===t.id&&frag)return frag;
    return enc(rel(s,tp))+frag;
  }
  // Only reuse actual output from the same verified operator; independent audits omit external cache.
  function indexFor(files,cache,sourceDigest){
    const records=Object.create(null),incoming=Object.create(null),outgoing=Object.create(null);
    for(const [id,text] of Object.entries(files)){const hash=digest(text),old=cache?.records?.[id];let edges;
      if(cache?.version===1&&old?.digest===hash&&Array.isArray(old.edges)&&old.edgeDigest===digest(JSON.stringify(old.edges))&&old.edges.every(e=>Number.isInteger(e.start)&&Number.isInteger(e.end)&&e.start>=0&&e.end>e.start&&text.slice(e.start,e.end)===e.raw&&JSON.stringify(e.parsed)===JSON.stringify(parse(e.raw,id))&&e.id===digest(JSON.stringify([id,e.start,e.end,e.raw])))){edges=old.edges;indexStats.reused++;}
      else{edges=refs(text).map(ref=>({...ref,parsed:parse(ref.raw,id),id:digest(JSON.stringify([id,ref.start,ref.end,ref.raw]))}));indexStats.parsed++;}
      records[id]={digest:hash,edges,edgeDigest:digest(JSON.stringify(edges))};outgoing[id]=[...new Set(edges.map(e=>e.parsed?.id).filter(Boolean))].sort();for(const to of outgoing[id]){if(!Object.hasOwn(incoming,to))incoming[to]=[];incoming[to].push(id);}
    }
    return {version:1,sourceDigest,records,incoming,outgoing};
  }
  const index=indexFor(before,referenceIndex,beforeDigest);
  function traverse(graph,root){const seen=new Set([root]),queue=[root];for(let i=0;i<queue.length;i++)for(const q of graph[queue[i]]||[])if(!seen.has(q)){seen.add(q);queue.push(q);}return queue.slice(1);}
  const closure=Object.fromEntries([...new Set(roots)].map(root=>[root,{incoming:traverse(index.incoming,root),outgoing:traverse(index.outgoing,root)}]));
  if(mode==="index")return {mode,beforeDigest,index,closure,indexStats,status:"INDEXED"};
  const repoSet=new Set([...Object.keys(before),...Object.keys(after)].map(k=>split(k)[0]));
  const expected=[];
  for(const [id,text] of Object.entries(before)){
    const source=dest(id);let out="",cursor=0;
    for(const ref of index.records[id].edges){
      const p=ref.parsed;if(!p){if(/github\.com/i.test(ref.raw))unchecked.push({source:id,raw:ref.raw,reason:"NON_MAIN_OR_UNSUPPORTED_GITHUB_URL"});continue;}
      if(!own(before,p.id)&&!own(moves,p.id)){if(repoSet.has(split(p.id)[0]))unchecked.push({source:id,raw:ref.raw,reason:"PREEXISTING_OR_UNADMITTED_TARGET"});else unchecked.push({source:id,raw:ref.raw,reason:"EXTERNAL_REPOSITORY"});continue;}
      const affected=source!==id||dest(p.id)!==p.id||own(anchors,p.id+"#"+p.anchor);
      const target=transform(p);if(!target)continue;
      const replacement=affected?format(p,target,source):ref.raw;
      expected.push({id:ref.id,source,target:target.id,anchor:target.anchor,affected,originalSource:id,originalTarget:p.id,originalAnchor:p.anchor,raw:ref.raw,referenceKind:ref.kind,start:ref.start,end:ref.end,disposition:source===target.id&&id!==p.id?"INTERNALISE_CANDIDATE":affected?"REDIRECT":"PRESERVE"});
      if(affected){out+=text.slice(cursor,ref.start)+replacement;cursor=ref.end;ledger.push({source:id,finalSource:source,old:ref.raw,new:replacement,target:target.id,anchor:target.anchor});}
    }
    if(cursor)edits[id]=out+text.slice(cursor);
  }
  if(mode==="audit"){
    const observed=new Map(),anchorCache=new Map();
    const knownPrevious=new Map();for(const [id,record] of Object.entries(index.records)){const set=new Set();for(const ref of record.edges){const p=ref.parsed;if(p)set.add(p.id+"#"+p.anchor);}knownPrevious.set(id,set);}
    const candidateIndex=indexFor(after,index,afterDigest);
    for(const [id,text] of Object.entries(after)){
      const set=new Set();observed.set(id,set);
      for(const ref of candidateIndex.records[id].edges){const p=ref.parsed;if(!p)continue;const key=p.id+"#"+p.anchor;set.add(key);
        if(!own(after,p.id)&&own(before,p.id))issues.push({kind:"DANGLING_PREVIOUS_TARGET",source:id,raw:ref.raw});
        else if(!own(after,p.id)&&repoSet.has(split(p.id)[0])&&!knownPrevious.get(id)?.has(key)&&!expected.some(e=>e.source===id&&e.target===p.id&&e.anchor===p.anchor))issues.push({kind:"NEW_UNRESOLVED_INTERNAL_TARGET",source:id,raw:ref.raw});
        if(own(after,p.id)&&p.anchor){if(!anchorCache.has(p.id))anchorCache.set(p.id,availableAnchors(after[p.id]));if(!anchorCache.get(p.id).has(p.anchor))issues.push({kind:"ANCHOR_UNVERIFIED",source:id,target:key});}
      }
      // Conservative residual scan catches code, comments, raw configuration and unparsed links.
      for(const old of retired){const [r,p]=split(old),base=p.split("/").pop();if(text.includes(old)||text.includes(p)||text.includes(enc(p))||text.includes(base)||text.includes(encodeURIComponent(base))){const review=literalReviews.find(x=>x.source===id&&x.target===old&&x.contentDigest===digest(text)&&x.reviewed===true&&typeof x.rationale==="string"&&x.rationale.trim());if(review)reviewedResiduals.push(review);else issues.push({kind:"RETIRED_PATH_LITERAL_REVIEW",source:id,target:old,contentDigest:digest(text)});}}
    }
    const usedReviews=new Set(),mappingDigest=digest(JSON.stringify([Object.entries(moves).sort(),Object.entries(anchors).sort()]));
    for(const e of expected){
      if(own(after,e.source)&&own(after,e.target)&&observed.get(e.source)?.has(e.target+"#"+e.anchor))continue;
      const review=relationshipReviews.find(q=>q.edgeId===e.id&&q.beforeDigest===beforeDigest&&q.afterDigest===afterDigest&&q.mappingDigest===mappingDigest&&q.reviewed===true&&typeof q.rationale==="string"&&q.rationale.trim()&&typeof q.authorization==="string"&&q.authorization.trim());
      let accepted=false;
      if(review&&own(after,e.source)&&own(after,e.target)&&e.affected){
        if(review.kind==="internalise"&&e.source===e.target&&e.originalSource!==e.originalTarget&&!e.anchor)accepted=true;
        if(review.kind==="subsumed"&&typeof review.replacementTarget==="string"&&typeof review.replacementAnchor==="string"&&own(after,review.replacementTarget)&&observed.get(e.source)?.has(review.replacementTarget+"#"+review.replacementAnchor))accepted=true;
        if(review.kind==="eliminate"&&review.nonoperative===true)accepted=true;
      }
      if(accepted){usedReviews.add(review.edgeId);reviewedRelationships.push({...review,edge:e});}else issues.push({...e,kind:"REFERENCE_NOT_PRESERVED",mappingDigest});
    }
    for(const q of relationshipReviews)if(!usedReviews.has(q.edgeId))issues.push({kind:"UNUSED_OR_STALE_RELATIONSHIP_REVIEW",edgeId:q.edgeId});
    for(const old of retired){if(own(after,old))issues.push({kind:"RETIRED_FILE_STILL_EXISTS",source:old});if(!own(after,dest(old)))issues.push({kind:"SURVIVOR_MISSING",target:dest(old)});}
  }
  return {mode,beforeDigest,afterDigest,moves,anchors,...(includeIndex?{index}:{}),closure,indexStats,edits,ledger,expected,unchecked,reviewedResiduals,reviewedRelationships,issues,status:issues.length?"OPEN":mode==="prepare"?"PREPARED":"SUPPORTED_REFERENCES_VERIFIED"};
}
export { digest, snapshot, dependency };
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try { console.log(JSON.stringify(dependency(JSON.parse(readFileSync(0, 'utf8'))),null,2)); }
  catch (error) { console.error(error.message); process.exitCode=1; }
}
