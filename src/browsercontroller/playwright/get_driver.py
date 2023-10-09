"""Gets the Playwright website controller and opens it. Prerequisites: pip
install pytest-playwright playwright install.

(Or with anaconda:) conda config --add channels conda-forge conda config
--add channels microsoft conda install playwright
"""

from typing import Optional

from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Browser, Page, Playwright
from playwright_stealth import stealth_sync
from typeguard import typechecked


@typechecked
def initialise_playwright_browsercontroller(
    start_url: str,
    browsertype: str,
    headless: Optional[bool] = False,
    stealthmode: Optional[bool] = True,
) -> tuple[Playwright, Page]:
    """Creates a Playwright browser, opens a new page, and navigates to a
    specified URL.

    Important, call playwright.stop() once you are done.

    Returns:
        tuple[Browser, Page]: A tuple containing the browser and page objects.
    """

    browser: Browser
    playwright: Playwright = sync_playwright().start()
    if browsertype == "firefox":
        browser = playwright.firefox.launch(headless=headless)
    if browsertype == "chromium":
        browser = playwright.chromium.launch(headless=headless)
    if browsertype == "safari":
        raise NotImplementedError("Error, did not implement webkit launch.")

    page: Page = browser.new_page()
    if stealthmode:
        stealth_sync(page)
    page.goto(start_url)

    return playwright, page
