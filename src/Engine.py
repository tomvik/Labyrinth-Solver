import asyncio
from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page

import Common


async def OpenLabyrinthGenerator(browser: Browser, headless: bool) -> Page:
    print("Opening labyrinth Generator page")

    browser = await launch(headless=headless, defaultViewport={'width': 1920, 'height': 1080})
    page: Page = await browser.newPage()

    await page.goto(Common.PAGE_URL)
    await page.screenshot({'path': 'data/main_page.png'})

    return page

def CloseBrowser(browser) -> None:
    asyncio.get_event_loop().run_until_complete(browser.close())   

def PlayGame():
    print("Playing game")

    browser = None
    page = None
    page = asyncio.get_event_loop().run_until_complete(OpenLabyrinthGenerator(browser, False))
    print(page)

    CloseBrowser(browser)

if __name__ == "__main__":
    Common.initialize_keyboard_listener()
    PlayGame()