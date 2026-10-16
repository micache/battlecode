// Read-only inspection of the locally served official visualiser.
// Playwright 1.56.1 and its matching headless Chromium are operator test tools.
const { chromium } = require('/opt/battlecode-check-tools/node_modules/playwright');
const fs = require('node:fs');
(async () => {
  const output = process.argv[2];
  const browser = await chromium.launch({headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage']});
  const cleanup = setTimeout(() => browser.close().finally(() => process.exit(2)), 60000);
  const context = await browser.newContext({viewport: {width: 900, height: 650}});
  await context.route('**/*', route => {
    const url = new URL(route.request().url());
    return ['127.0.0.1', 'localhost'].includes(url.hostname) ? route.continue() : route.abort();
  });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  await page.goto('http://127.0.0.1:7026/?replay=replay.zip&cambc-cli=1');
  await page.waitForTimeout(10000);
  await page.keyboard.press('End');
  await page.waitForTimeout(1000);
  const report = {url: page.url(), body: await page.locator('body').innerText(),
                  buttons: await page.getByRole('button').evaluateAll(elements => elements.map(e => ({text:e.textContent, title:e.title, aria:e.getAttribute('aria-label')}))),
                  inputs: await page.locator('input').evaluateAll(elements => elements.map(e => ({type:e.type,min:e.min,max:e.max,value:e.value,aria:e.getAttribute('aria-label')}))), errors};
  fs.writeFileSync(output + '.json', JSON.stringify(report, null, 2));
  try { await page.screenshot({path: output + '.png', fullPage: true, timeout: 5000}); } catch (error) { report.screenshotError=String(error); }
  console.log(JSON.stringify(report));
  await browser.close();
  clearTimeout(cleanup);
})().catch(error => {console.error(error); process.exit(1);});
