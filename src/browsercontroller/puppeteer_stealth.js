// One can also silently login to a website using puppeteer stealth mode.
// This entails the following prerequisites:
// 1. Install puppeteer:
// npm install puppeteer
// 2. Install plugins: that give it the stealth modes:
// npm install puppeteer-extra-plugin-stealth
// npm install puppeteer puppeteer-extra puppeteer-extra-plugin-stealth
// 3. Run this script with:
// node puppeteer_stealth.js

//const puppeteer = require('puppeteer');
const readline = require('readline');

// make it stealth mode
const puppeteer = require('puppeteer-extra')

// add stealth plugin and use defaults (all evasion techniques)
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
puppeteer.use(StealthPlugin())

// Create a readline interface for reading user input from the CLI
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

async function main() {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 720 });
  await page.goto('https://chat.openai.com/auth/login', { waitUntil: 'domcontentloaded' }); // wait until DOMContentLoaded

  // Ask the user to input "proceed" in the CLI
  rl.question('Please enter "proceed" in the CLI and press Enter when ready: ', async (answer) => {
    if (answer.trim().toLowerCase() === 'proceed') {
      // User entered "proceed," continue with the script
      await page.type('#id', "CREDS.username");
      await page.type('#loginPw', CREDS.password);

      // click and wait for navigation
      await Promise.all([
        page.click('#loginSubmit'),
        page.waitForNavigation({ waitUntil: 'domcontentloaded' }),
      ]);

      // Close the readline interface
      rl.close();
      await browser.close();
    } else {
      console.log('Please enter "proceed" to continue.');
      // Close the readline interface
      rl.close();
      await browser.close();
    }
  });
}

main();
