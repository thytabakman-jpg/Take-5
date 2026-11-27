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
function decompile(input) {
  const {files,history=[],maxPairs=50000,threshold=.7}=input;
  if(!Number.isInteger(maxPairs)||maxPairs<0||!(threshold>0&&threshold<=1))throw Error("Invalid comparison parameters");
  const sourceDigest=snapshot(files),units=[],sources=[];
  function extract(source,text,historical){
    if(typeof text!=="string"||typeof source!=="string")throw Error("Invalid source");
    sources.push({source,historical,digest:digest(text),length:text.length});
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
    if(units.filter(u=>u.source===source&&u.historical===historical).map(u=>u.text).join("")!==text)throw Error("Round-trip failed: "+source);
  }
  for(const id of Object.keys(files).sort())extract(id,files[id],false);
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
  return {sourceDigest,sources,units,exactGroups:[...exact.values()].filter(g=>g.length>1),similar,compared,comparisonComplete:exhausted,semanticStatus:"UNASSESSED"};
}
export { digest, snapshot, decompile };
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try { console.log(JSON.stringify(decompile(JSON.parse(readFileSync(0, 'utf8'))),null,2)); }
  catch (error) { console.error(error.message); process.exitCode=1; }
}
