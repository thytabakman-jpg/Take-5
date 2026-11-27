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
function discover(input){
  const {files,targets=Object.keys(files||{}),metadata={},maxPairs=50000,threshold=.25,maxPosting=250}=input;
  const sourceDigest=snapshot(files);
  if(!Array.isArray(targets)||new Set(targets).size!==targets.length||targets.some(id=>!Object.hasOwn(files,id))||!Number.isInteger(maxPairs)||maxPairs<0||!Number.isInteger(maxPosting)||maxPosting<2||!(threshold>0&&threshold<=1))throw Error("Invalid discovery scope or budget");
  const tokenize=s=>new Set(s.toLowerCase().match(/[\p{L}\p{N}]+/gu)||[]);
  const ids=[...targets].sort(),groups=new Map(),postings=new Map(),features=new Map(),pairs=new Map(),skippedTokens=[];
  for(const id of ids){const text=files[id],key=digest(text);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(id);const tokens=tokenize(text);features.set(id,tokens);for(const token of tokens){if(!postings.has(token))postings.set(token,[]);postings.get(token).push(id);}}
  const exactGroups=[...groups.values()].flatMap(g=>{const byText=new Map();for(const id of g){const x=files[id];if(!byText.has(x))byText.set(x,[]);byText.get(x).push(id);}return [...byText.values()].filter(x=>x.length>1);});
  let budgetHit=false;
  outer:for(const [token,rows] of [...postings].sort((a,b)=>a[1].length-b[1].length||a[0].localeCompare(b[0]))){if(rows.length>maxPosting){skippedTokens.push({token,frequency:rows.length});continue;}for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++){const k=JSON.stringify([rows[i],rows[j]]);if(!pairs.has(k)){if(pairs.size>=maxPairs){budgetHit=true;break outer;}pairs.set(k,[rows[i],rows[j]]);}}}
  const similarity=(a,b)=>{if(!Array.isArray(a)||!Array.isArray(b)||!a.length||!b.length)return null;const x=new Set(a),y=new Set(b);let n=0;for(const q of x)if(y.has(q))n++;return n/(x.size+y.size-n);};
  const candidates=[];
  for(const [a,b] of pairs.values()){const x=features.get(a),y=features.get(b);let shared=0;for(const k of x)if(y.has(k))shared++;const info=shared/(x.size+y.size-shared),containment=Math.max(shared/x.size,shared/y.size);const role=similarity(metadata[a]?.roles,metadata[b]?.roles),deps=similarity(metadata[a]?.dependencies,metadata[b]?.dependencies);const available=[[info,6],[role,2],[deps,2]].filter(([n])=>n!==null),score=available.reduce((s,[n,w])=>s+n*w,0)/available.reduce((s,[n,w])=>s+w,0);if(info>=threshold||containment>=.8||score>=threshold)candidates.push({a,b,score,information:info,responsibility:role,dependency:deps,containment,residualA:x.size-shared,residualB:y.size-shared,disposition:"REVIEW_ONLY"});}
  candidates.sort((a,b)=>b.score-a.score||b.containment-a.containment||a.a.localeCompare(b.a)||a.b.localeCompare(b.b));
  const parent=new Map(ids.map(x=>[x,x]));function find(x){while(parent.get(x)!==x){parent.set(x,parent.get(parent.get(x)));x=parent.get(x);}return x;}function union(a,b){parent.set(find(b),find(a));}
  for(const g of exactGroups)for(const id of g.slice(1))union(g[0],id);for(const q of candidates)union(q.a,q.b);
  const clusters=new Map();for(const id of ids){const k=find(id);if(!clusters.has(k))clusters.set(k,[]);clusters.get(k).push(id);}
  return {mode:"discover",sourceDigest,exactGroups,candidates,groups:[...clusters.values()].filter(g=>g.length>1),compared:pairs.size,skippedTokens,budgetHit,comparisonComplete:!budgetHit&&!skippedTokens.length,semanticStatus:"UNASSESSED"};
}
function decompile(input) {
  if(input.mode==='discover')return discover(input);
  if(input.mode&&input.mode!=='decompose')throw Error('Unknown decompiler mode');
  const {files,history=[],targets=Object.keys(files||{}),maxPairs=50000,threshold=.7,includeWorking=true,taxonomy={definitions:['definition','defined as','means'],claims:['claim','proposition','assertion','thesis'],evidence:['evidence','citation','source','witness'],arguments:['inference','therefore','premise','argument'],mathematics:['theorem','equation','operator','proof'],methods:['method','procedure','protocol'],architecture:['architecture','dependency','responsibility'],history:['historical','legacy','superseded'],questions:['unresolved','question','open problem']}}=input;
  if(!Number.isInteger(maxPairs)||maxPairs<0||!(threshold>0&&threshold<=1))throw Error("Invalid comparison parameters");
  const sourceDigest=snapshot(files),units=[],sources=[];
  if(!Array.isArray(targets)||new Set(targets).size!==targets.length||targets.some(id=>!Object.prototype.hasOwnProperty.call(files,id)))throw Error("Invalid target selection");
  function extract(source,text,historical){
    if(typeof text!=="string"||typeof source!=="string")throw Error("Invalid source");
    sources.push({source,historical,digest:digest(text),length:text.length});
    const first=units.length;
    const lines=text.match(/[^\n]*\n|[^\n]+$/g)||[];
    let pos=0,start=0,buf="",kind="text",fence=null;
    function flush(){if(!buf)return;units.push({id:digest(JSON.stringify([source,start,pos,historical])),source,start,end:pos,kind,text:buf,historical});buf="";start=pos;kind="text";}
    for(const line of lines){
      const m=line.match(/^ {0,3}(`{3,}|~{3,})/);
      if(fence){buf+=line;pos+=line.length;if(m&&m[1][0]===fence[0]&&m[1].length>=fence.length&&/^ {0,3}(`{3,}|~{3,})\s*$/.test(line)){fence=null;flush();}continue;}
      if(m){flush();kind="code";fence=m[1];buf=line;pos+=line.length;continue;}
      if(/^ {0,3}#{1,6}\s/.test(line)){flush();kind="heading";buf=line;pos+=line.length;flush();continue;}
      if(!line.trim()){flush();kind="separator";buf=line;pos+=line.length;flush();continue;}
      if(!buf)kind=/^\s*\|/.test(line)?"table":/^\s*(?:[-*+]|\d+\.)\s/.test(line)?"list":"text";
      buf+=line;pos+=line.length;
    }flush();
    if(units.slice(first).map(u=>u.text).join("")!==text)throw Error("Round-trip failed: "+source);
  }
  for(const id of [...targets].sort())extract(id,files[id],false);
  const historicalIds=new Set();for(const h of history){if(!h||historicalIds.has(h.id))throw Error("Duplicate history identity");historicalIds.add(h.id);extract(h.id,h.text,true);}
  const exact=new Map(),representatives=[],similar=[];
  for(const u of units){if(u.kind==="separator")continue;const key=JSON.stringify([u.kind,u.text]);if(!exact.has(key)){exact.set(key,[]);representatives.push(u);}exact.get(key).push(u.id);}
  const tokenize=s=>new Set(s.toLowerCase().match(/[\p{L}\p{N}]+/gu)||[]);
  const tokens=representatives.map(u=>tokenize(u.text));
  let compared=0,exhausted=true;
  outer:for(let i=0;i<representatives.length;i++)for(let j=i+1;j<representatives.length;j++){
    if(compared>=maxPairs){exhausted=false;break outer;}compared++;
    const a=representatives[i],b=representatives[j];if(a.kind!==b.kind)continue;
    let overlap=0;for(const t of tokens[i])if(tokens[j].has(t))overlap++;
    const union=tokens[i].size+tokens[j].size-overlap,score=union?overlap/union:0;
    if(score>=threshold)similar.push({a:a.id,b:b.id,score,disposition:"REVIEW_ONLY"});
  }
  const layers={},layerByUnit={},bySource=new Map();
  if(!taxonomy||typeof taxonomy!=="object"||Array.isArray(taxonomy)||Object.entries(taxonomy).some(([k,v])=>!k||!Array.isArray(v)||v.some(s=>typeof s!=="string"||!s.trim())))throw Error("Invalid taxonomy");
  for(const u of units){const key=JSON.stringify([u.source,u.historical]);if(!bySource.has(key))bySource.set(key,[]);bySource.get(key).push(u);const tags=["structure:"+u.kind];const lower=u.text.toLowerCase();if(u.historical)tags.push("semantic:history");if(u.kind!=="separator"&&u.kind!=="code"){for(const [tag,words] of Object.entries(taxonomy))if(words.some(w=>lower.includes(w.toLowerCase())))tags.push("semantic:"+tag);if(!tags.some(x=>x.startsWith("semantic:")))tags.push("semantic:unresolved");}layerByUnit[u.id]=[...new Set(tags)];for(const tag of layerByUnit[u.id]){if(!Object.hasOwn(layers,tag))layers[tag]=[];layers[tag].push(u.id);}}
  const unitById=new Map(units.map(u=>[u.id,u]));
  const working=includeWorking?{consolidated:sources.map(s=>"## SOURCE "+JSON.stringify(s.source)+" ["+s.digest+"]\n\n"+(bySource.get(JSON.stringify([s.source,s.historical]))||[]).map(u=>u.text).join("")).join("\n\n"),layered:Object.entries(layers).map(([k,ids])=>"## "+k+"\n\n"+ids.map(id=>{const u=unitById.get(id);return "SOURCE "+JSON.stringify(u.source)+" ["+u.start+","+u.end+") "+id+"\n"+u.text;}).join("\n\n")).join("\n\n")}:undefined;
  const layerComparisons=Object.fromEntries(Object.entries(layers).filter(([k])=>k.startsWith("semantic:")).map(([k,ids])=>{const set=new Set(ids);return [k,similar.filter(q=>set.has(q.a)&&set.has(q.b))];}));
  const currentExact=new Set(units.filter(u=>!u.historical&&u.kind!=="separator").map(u=>u.text)),historicResidual=units.filter(u=>u.historical&&u.kind!=="separator"&&!currentExact.has(u.text)).map(u=>u.id);
  const timeline=new Map();for(const h of history){if(typeof h.file==="string"&&Number.isInteger(h.order)){if(!timeline.has(h.file))timeline.set(h.file,[]);timeline.get(h.file).push(h);}}
  const historicalChanges=[];for(const [file,rows] of timeline){rows.sort((a,b)=>a.order-b.order);if(new Set(rows.map(q=>q.order)).size!==rows.length)throw Error("Ambiguous history order");const get=(id,historical)=>(bySource.get(JSON.stringify([id,historical]))||[]).filter(u=>u.kind!=="separator");const seq=rows.map(h=>({id:h.id,units:get(h.id,true)}));if(targets.includes(file))seq.push({id:file,units:get(file,false)});for(let i=1;i<seq.length;i++){const a=seq[i-1],b=seq[i],aa=new Set(a.units.map(u=>u.text)),bb=new Set(b.units.map(u=>u.text));historicalChanges.push({file,from:a.id,to:b.id,added:b.units.filter(u=>!aa.has(u.text)).map(u=>u.id),removed:a.units.filter(u=>!bb.has(u.text)).map(u=>u.id)});}}
  return {sourceDigest,targets:[...targets].sort(),sources,units,layers,layerByUnit,layerComparisons,working,historicResidual,historicalChanges,exactGroups:[...exact.values()].filter(g=>g.length>1),similar,compared,comparisonComplete:exhausted,semanticStatus:"UNASSESSED"};
}
export { digest, snapshot, decompile };
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try { console.log(JSON.stringify(decompile(JSON.parse(readFileSync(0, 'utf8'))),null,2)); }
  catch (error) { console.error(error.message); process.exitCode=1; }
}
