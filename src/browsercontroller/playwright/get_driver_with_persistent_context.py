"""Gets the Playwright website controller and opens it. Prerequisites: pip
install pytest-playwright playwright install.

(Or with anaconda:) conda config --add channels conda-forge conda config
--add channels microsoft conda install playwright
"""

from typing import Optional, Tuple

from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import BrowserContext, Page, Playwright
from playwright_stealth import stealth_sync
from typeguard import typechecked


@typechecked
def initialise_playwright_browsercontroller_with_context(
    start_url: str,
    browsertype: str,
    headless: Optional[bool] = False,
    stealthmode: Optional[bool] = True,
    user_data_dir: Optional[
        str
    ] = None,  # Optional parameter to pass saved cookies
) -> Tuple[Playwright, Page]:
    """Creates a Playwright browser, opens a new page, and navigates to a
    specified URL.

    Important, call playwright.stop() once you are done.

    Returns:
        tuple[Browser, Page]: A tuple containing the browser and page objects.
    """
    page: Page
    browser: BrowserContext
    playwright: Playwright = sync_playwright().start()
    if browsertype == "firefox":
        browser = playwright.firefox.launch_persistent_context(
            user_data_dir=user_data_dir, headless=headless
        )
    if browsertype == "chromium":
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir, headless=headless
        )
    if browsertype == "safari":
        raise NotImplementedError("Error, did not implement webkit launch.")

    if len(browser.pages) == 0:
        page = browser.new_page()
    else:
        page = browser.pages[0]

    if stealthmode:
        stealth_sync(page)
    page.goto(start_url)
    return playwright, page
