// Diagnostic only: save actual UI state even when full replay review cannot finish.
const {chromium} = require('/opt/battlecode-check-tools/node_modules/playwright');
const fs = require('node:fs');
(async () => {
 const browser = await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,
   args:['--no-sandbox','--disable-dev-shm-usage','--enable-unsafe-swiftshader']});
 const context = await browser.newContext({viewport:{width:900,height:650}});
 await context.route('**/*', route => ['127.0.0.1','localhost'].includes(new URL(route.request().url()).hostname)
   ? route.continue() : route.abort());
 const page = await context.newPage();
 const errors=[];
 page.on('pageerror', e => errors.push(String(e)));
 await page.goto('http://127.0.0.1:7026/?replay=replay.zip&cambc-cli=1');
 await page.waitForTimeout(3000);
 const report={body:await page.locator('body').innerText(),errors,
   inputs:await page.locator('input').evaluateAll(es=>es.map(e=>({type:e.type,max:e.max,value:e.value,aria:e.getAttribute('aria-label')}))),
   storage:await page.evaluate(()=>({...localStorage}))};
 fs.writeFileSync(process.argv[2],JSON.stringify(report,null,2));
 console.log(JSON.stringify(report));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
