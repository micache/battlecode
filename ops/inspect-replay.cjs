// Read-only inspection of the locally served official visualiser.
// Playwright 1.56.1 and its matching headless Chromium are operator test tools.
const { chromium } = require('/opt/battlecode-check-tools/node_modules/playwright');
const fs = require('node:fs');
(async () => {
  const output = process.argv[2];
  const expectedRound = Number(process.argv[3]);
  const port = Number(process.argv[4] || 7026);
  if (!Number.isInteger(port) || port < 1024 || port > 65535) throw new Error('invalid local review port');
  if (!Number.isInteger(expectedRound) || expectedRound < 1) throw new Error('expected final statistics round required');
  const browser = await chromium.launch({headless: true,
    executablePath: fs.existsSync('/usr/bin/chromium') ? '/usr/bin/chromium' : undefined,
    args: ['--no-sandbox', '--disable-dev-shm-usage']});
  const cleanup = setTimeout(() => browser.close().finally(() => process.exit(2)), 120000);
  const context = await browser.newContext({viewport: {width: 900, height: 650}});
  await context.route('**/*', route => {
    const url = new URL(route.request().url());
    return ['127.0.0.1', 'localhost'].includes(url.hostname) ? route.continue() : route.abort();
  });
  const page = await context.newPage();
  await page.addInitScript(() => {
    localStorage.setItem('cambc.graphics.mode', 'manual');
    localStorage.setItem('cambc.graphics.v1', JSON.stringify({renderScale:50,ground:'simple',groundResolution:25,
      bloom:false,antialiasing:false,shadows:false,foliageDensity:25,decorativeFoliage:false,
      foliageSway:false,bushWindows:false,mapBackdrop:false}));
  });
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  const origin = `http://127.0.0.1:${port}`;
  let replayHash;
  if (process.argv[5]) {
    const response = await context.request.get(origin + '/replay.zip');
    if (!response.ok()) throw new Error('served replay unavailable');
    const bytes = await response.body();
    if (bytes.length > 64 * 1024 * 1024) throw new Error('served replay exceeds bound');
    replayHash = require('node:crypto').createHash('sha256').update(bytes).digest('hex');
    if (replayHash !== process.argv[5]) throw new Error('visualizer is serving a different replay');
  }
  await page.goto(origin + '/?replay=replay.zip&cambc-cli=1');
  try { await page.waitForFunction(round => {
    const range = document.querySelector('input[aria-label^="Seek timeline"]');
    return range && Number(range.max) >= round && !document.body.innerText.includes('Loading timeline...');
  }, expectedRound, {timeout:90000}); } catch (error) {
    fs.writeFileSync(output + '-incomplete.json', JSON.stringify({body: await page.locator('body').innerText(),
      inputs: await page.locator('input').evaluateAll(elements => elements.map(e => ({type:e.type,min:e.min,max:e.max,value:e.value,aria:e.getAttribute('aria-label')}))),
      errors}, null, 2));
    throw error;
  }
  const seek = page.locator('input[aria-label^="Seek timeline"]');
  await seek.focus();
  await page.keyboard.press('End');
  await page.waitForTimeout(2000);
  const report = {url: page.url(), served_replay_sha256: replayHash, body: await page.locator('body').innerText(),
                  buttons: await page.getByRole('button').evaluateAll(elements => elements.map(e => ({text:e.textContent, title:e.title, aria:e.getAttribute('aria-label')}))),
                  inputs: await page.locator('input').evaluateAll(elements => elements.map(e => ({type:e.type,min:e.min,max:e.max,value:e.value,aria:e.getAttribute('aria-label')}))), errors};
  fs.writeFileSync(output + '.json', JSON.stringify(report, null, 2));
  try { await page.screenshot({path: output + '.png', fullPage: true, timeout: 5000}); } catch (error) { report.screenshotError=String(error); }
  console.log(JSON.stringify(report));
  await browser.close();
  clearTimeout(cleanup);
})().catch(error => {console.error(error); process.exit(1);});
