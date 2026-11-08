const {chromium}=require('playwright');(async()=>{
const [url,out,a,bEnd]=process.argv.slice(2);
const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--use-gl=angle']});
const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto(url+'?clean=1');await p.waitForFunction('window.OPENER&&window.OPENER.ready',{timeout:60000});
const D=await p.evaluate(()=>window.OPENER.DURATION);const N=Math.round(D*30);require('fs').mkdirSync(out,{recursive:true});
for(let i=+a;i<Math.min(N,+bEnd);i++){await p.evaluate(t=>window.OPENER.seek(t),i/30);
 await p.screenshot({path:`${out}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:93});if(i%50==0)console.log(i);}
console.log('done',N);await b.close();})();
