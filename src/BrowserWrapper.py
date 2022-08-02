import asyncio
import time
from typing import Tuple
from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page
from pyppeteer.element_handle import ElementHandle

from Common import Print
import Common

async def OpenLabyrinthGenerator(headless: bool) -> Tuple[Browser, Page, bool]:
    print("Opening labyrinth Generator page")
    ok = False

    try:
        browser = await launch(headless=headless, defaultViewport={'width': 1920, 'height': 1080})
        page: Page = await browser.newPage()

        await page.goto(Common.PAGE_URL)
        await page.screenshot({'path': 'data/main_page.png'})

        ok = True
    except Exception as e:
        Print('OpenLabyrinthGenerator', e)

    return browser, page, ok

async def CloseBrowser(browser: Browser) -> None:
    if browser is not None:
        await browser.close()
        browser = None

async def GetPageElement(page: Page, query: str) -> ElementHandle:
    element = await page.J(query)

    if element is None:
        raise TypeError("Element not found. Query: {}".format(query))

    return element

async def GetRowsAndColumnsInputElement(page: Page) -> Tuple[ElementHandle, ElementHandle, bool]:
    ok = False
    try:
        rows_input_element = await GetPageElement(page, Common.ROWS_ELEMENT_QUERY)
        columns_input_element = await GetPageElement(page, Common.COLUMNS_ELEMENT_QUERY)

        ok = True
    except TypeError as e:
        Print('GetRowsAndColumnsInputElement', 'An input element was not found. Verify the page and query are correct. {}'.format(e))
    except Exception as e:
        Print('GetRowsAndColumnsInputElement', 'Unknown error occured. {}'.format(e))

    return rows_input_element, columns_input_element, ok

async def WriteInputValue(element: ElementHandle, txt: str) -> None:
    try:
        await element.click({'clickCount': 2,
                             'delay': 10})
        await element.type(txt)
    except TypeError as e:
        Print('WriteInputValue', e)
        raise e
    except Exception as e:
        Print('WriteInputValue', 'Unknown error: {}'.format(e))
        raise e

async def WriteRowsAndColumns(rows_input: ElementHandle, columns_input: ElementHandle, num_rows: int, num_columns: int) -> bool:
    ok = False
    try:
        await WriteInputValue(rows_input, str(num_rows))
        await WriteInputValue(columns_input, str(num_columns))

        ok = True
    except Exception as e:
        Print('WriteRowsAndColumns', e)

    return ok

async def ClickSubmit(page: Page) -> bool:
    ok = False

    try:
        submit_element = await GetPageElement(page, Common.SUBMIT_ELEMENT_QUERY)

        await submit_element.click()

        time.sleep(5)

        ok = True
    except TypeError as e:
        Print('ClickSubmit', 'The submit button was not found. {}'.format(e))
    except Exception as e:
        Print('ClickSubmit', 'Unknown error occured. {}'.format(e))

    return ok

async def GetLabyrinthImageAndStoreIt(page: Page, labyrinth_path: str) -> bool:
    ok = False

    try:
        image_block_element = await GetPageElement(page, Common.IMAGE_BLOCK_ELEMENT_QUERY)

        image_element: ElementHandle = await image_block_element.J('img')

        await image_element.screenshot({'path': labyrinth_path})

        ok = True
    except TypeError as e:
        Print('GetLabyrinthImageAndStoreIt', 'The image block was not found. {}'.format(e))
    except Exception as e:
        Print('GetLabyrinthImageAndStoreIt', 'Unknown error occured. {}'.format(e))

    return ok


async def AsyncOpenBrowserAndStoreCustomLabyrinth(num_rows: int, num_columns: int, labyrinth_path: str) -> bool:
    print("Playing game")

    ok: bool = False
    browser: Browser = None
    page: Page = None
    browser, page, ok = await OpenLabyrinthGenerator(False)

    if not ok:
        return

    rows_input: ElementHandle = None
    columns_input: ElementHandle = None
    rows_input, columns_input, ok = await GetRowsAndColumnsInputElement(page)

    if not ok:
        await CloseBrowser(browser)
        return

    ok = await WriteRowsAndColumns(rows_input, columns_input, num_rows, num_columns)

    if not ok:
        await CloseBrowser(browser)
        return

    ok = await ClickSubmit(page)

    if not ok:
        await CloseBrowser(browser)
        return

    await page.screenshot({'path': 'data/main_page_after_input.png'})

    ok = await GetLabyrinthImageAndStoreIt(page, labyrinth_path)

    await CloseBrowser(browser)
    
    return ok

def OpenBrowserAndStoreCustomLabyrinth(num_rows, num_columns, labyrinth_path):
    asyncio.get_event_loop().run_until_complete(AsyncOpenBrowserAndStoreCustomLabyrinth(num_rows, num_columns, labyrinth_path))