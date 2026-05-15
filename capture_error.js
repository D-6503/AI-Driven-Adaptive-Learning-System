const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

  console.log('Navigating to Home...');
  await page.goto('http://localhost:5173/');
  await new Promise(r => setTimeout(r, 2000));

  // If there's an error on results, we'd have to navigate there.
  // Assuming session 1 exists.
  console.log('Navigating to Results...');
  await page.goto('http://localhost:5173/results/1');
  await new Promise(r => setTimeout(r, 2000));

  await browser.close();
})();
