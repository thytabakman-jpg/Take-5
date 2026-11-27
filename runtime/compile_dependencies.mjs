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
function dependency(input){
  const {before,after=before,moves={},anchors={},mode="prepare"}=input;
  const beforeDigest=snapshot(before),afterDigest=snapshot(after);
  if(!["prepare","audit"].includes(mode))throw Error("Unknown mode");
  const issues=[],edits={},ledger=[],unchecked=[];
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
        occupied.push([start,end]);result.push({start:offset+start,end:offset+end,raw});
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
  const repoSet=new Set([...Object.keys(before),...Object.keys(after)].map(k=>split(k)[0]));
  const expected=[];
  for(const [id,text] of Object.entries(before)){
    const source=dest(id);let out="",cursor=0;
    for(const ref of refs(text)){
      const p=parse(ref.raw,id);if(!p){if(/github\.com/i.test(ref.raw))unchecked.push({source:id,raw:ref.raw,reason:"NON_MAIN_OR_UNSUPPORTED_GITHUB_URL"});continue;}
      if(!own(before,p.id)&&!own(moves,p.id)){if(repoSet.has(split(p.id)[0]))unchecked.push({source:id,raw:ref.raw,reason:"PREEXISTING_OR_UNADMITTED_TARGET"});else unchecked.push({source:id,raw:ref.raw,reason:"EXTERNAL_REPOSITORY"});continue;}
      const affected=source!==id||dest(p.id)!==p.id||own(anchors,p.id+"#"+p.anchor);
      const target=transform(p);if(!target)continue;
      const replacement=affected?format(p,target,source):ref.raw;
      expected.push({source,target:target.id,anchor:target.anchor,affected,originalSource:id,raw:ref.raw});
      if(affected){out+=text.slice(cursor,ref.start)+replacement;cursor=ref.end;ledger.push({source:id,finalSource:source,old:ref.raw,new:replacement,target:target.id,anchor:target.anchor});}
    }
    if(cursor)edits[id]=out+text.slice(cursor);
  }
  if(mode==="audit"){
    const observed=new Map(),anchorCache=new Map();
    for(const [id,text] of Object.entries(after)){
      const set=new Set();observed.set(id,set);
      for(const ref of refs(text)){const p=parse(ref.raw,id);if(!p)continue;const key=p.id+"#"+p.anchor;set.add(key);
        if(!own(after,p.id)&&own(before,p.id))issues.push({kind:"DANGLING_PREVIOUS_TARGET",source:id,raw:ref.raw});
        if(own(after,p.id)&&p.anchor){if(!anchorCache.has(p.id))anchorCache.set(p.id,availableAnchors(after[p.id]));if(!anchorCache.get(p.id).has(p.anchor))issues.push({kind:"ANCHOR_UNVERIFIED",source:id,target:key});}
      }
      // Conservative residual scan catches code, comments, raw configuration and unparsed links.
      for(const old of retired){const [r,p]=split(old),base=p.split("/").pop();if(text.includes(old)||text.includes(p)||text.includes(enc(p))||text.includes(base)||text.includes(encodeURIComponent(base)))issues.push({kind:"RETIRED_PATH_LITERAL_REVIEW",source:id,target:old});}
    }
    for(const e of expected){if(!own(after,e.source)||!own(after,e.target)||!observed.get(e.source)?.has(e.target+"#"+e.anchor))issues.push({kind:"REFERENCE_NOT_PRESERVED",...e});}
    for(const old of retired){if(own(after,old))issues.push({kind:"RETIRED_FILE_STILL_EXISTS",source:old});if(!own(after,dest(old)))issues.push({kind:"SURVIVOR_MISSING",target:dest(old)});}
  }
  return {mode,beforeDigest,afterDigest,edits,ledger,expected,unchecked,issues,status:issues.length?"OPEN":mode==="prepare"?"PREPARED":"SUPPORTED_REFERENCES_VERIFIED"};
}
export { digest, snapshot, dependency };
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try { console.log(JSON.stringify(dependency(JSON.parse(readFileSync(0, 'utf8'))),null,2)); }
  catch (error) { console.error(error.message); process.exitCode=1; }
}
