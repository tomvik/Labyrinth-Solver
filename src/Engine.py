import asyncio
from typing import Tuple
from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page
from pyppeteer.element_handle import ElementHandle

import Common

def Print(function_name: str, message: str):
    print('[{}]: {}'.format(function_name, message))

async def OpenLabyrinthGenerator(headless: bool) -> Page:
    print("Opening labyrinth Generator page")

    browser = await launch(headless=headless, defaultViewport={'width': 1920, 'height': 1080})
    page: Page = await browser.newPage()

    await page.goto(Common.PAGE_URL)
    await page.screenshot({'path': 'data/main_page.png'})

    return browser, page

async def CloseBrowser(browser: Browser) -> None:
    if browser is not None:
        await browser.close()
        browser = None

async def GetPageElement(page: Page, query: str) -> ElementHandle:
    element = await page.J(query)

    if element is None:
        raise TypeError("Element not found. Query: {}".format(query))

    return element

async def GetInputElements(page: Page) -> Tuple[ElementHandle, ElementHandle]:
    try:
        rows_input_element = await GetPageElement(page, '[name="zeilenstr"]')
        columns_input_element = await GetPageElement(page, '[name="spaltenstr"]')
    except TypeError as e:
        Print('GetInputElements', 'An input element was not found. Verify the page and query are correct. {}'.format(e))
        raise e
    except Exception as e:
        Print('GetInputElements', 'Unkown error occured. {}'.format(e))
        raise e

    return rows_input_element, columns_input_element

async def PlayGame():
    print("Playing game")

    browser: Browser = None
    page: Page = None
    try:
        browser, page = await OpenLabyrinthGenerator(False)
    except:
        Print('PlayGame', 'Failed opening the webpage')
        return

    rows_input: ElementHandle = None
    columns_input: ElementHandle = None
    try:
        rows_input, columns_input = await GetInputElements(page)
    except TypeError as e:
        Print('PlayGame', 'GetInputElements failed. {}'.format(e))
        await CloseBrowser(browser)
    except Exception as e:
        Print('PlayGame', 'Unkown error occured. {}'.format(e))
        await CloseBrowser(browser)

    await CloseBrowser(browser)
    

if __name__ == "__main__":
    Common.initialize_keyboard_listener()
    asyncio.run(PlayGame())