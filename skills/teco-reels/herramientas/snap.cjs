const { chromium } = require('playwright');
(async()=>{
 const [dir, out, ...times]=process.argv.slice(2);
 const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--use-gl=angle']}); const p=await b.newPage({viewport:{width:1080,height:1920}});
 p.on('pageerror',e=>console.log('ERR',e.message)); p.on('console',m=>{if(m.type()==='error')console.log('CONSOLE',m.text())});
 await p.goto('file://'+dir+'/index.html?clean=1'); await p.waitForFunction('window.OPENER&&window.OPENER.ready',{timeout:30000});
 require('fs').mkdirSync(out,{recursive:true});
 for(const ts of times){ const t=+ts; await p.evaluate(t=>{window.OPENER.seek(t);},t); await p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
   await p.screenshot({path:`${out}/t${t.toFixed(2)}.png`}); }
 await b.close();
})();
