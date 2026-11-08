const { chromium } = require('playwright');
(async()=>{
 const [dir,out,fpsS]=process.argv.slice(2); const FPS=+(fpsS||30);
 const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--use-gl=angle']}); const p=await b.newPage({viewport:{width:1080,height:1920}});
 p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+dir+'/index.html?clean=1'); await p.waitForFunction('window.OPENER&&window.OPENER.ready',{timeout:30000});
 const D=await p.evaluate(()=>window.OPENER.DURATION); const N=Math.round(D*FPS);
 require('fs').mkdirSync(out,{recursive:true});
 for(let i=0;i<N;i++){ await p.evaluate(t=>window.OPENER.seek(t),i/FPS); await p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
   await p.screenshot({path:`${out}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:95}); if(i%60==0)process.stdout.write(i+' '); }
 console.log('done',N); await b.close();
})();
