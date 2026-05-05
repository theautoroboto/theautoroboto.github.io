import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to the page
        await page.goto("http://localhost:8000/seniority-paradox.html")

        # Make sure the directory exists
        os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

        # Take screenshot
        await page.screenshot(path="/home/jules/verification/screenshots/seniority-paradox.png", full_page=True)

        await browser.close()

asyncio.run(main())
