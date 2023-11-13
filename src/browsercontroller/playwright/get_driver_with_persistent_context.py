"""Gets the Playwright website controller and opens it. Prerequisites: pip
install pytest-playwright playwright install.

(Or with anaconda:) conda config --add channels conda-forge conda config
--add channels microsoft conda install playwright
"""

from typing import Optional, Tuple

from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import (
    BrowserContext,
    Page,
    Playwright,
    Video,
)
from playwright_stealth import stealth_sync
from typeguard import typechecked


@typechecked
def init_playwright_with_context(
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
    playwright: Playwright
    page: Page
    playwright, page = get_page(
        browsertype=browsertype,
        headless=headless,
        stealthmode=stealthmode,
        user_data_dir=user_data_dir,
    )
    page.goto(start_url)

    return playwright, page


@typechecked
def init_playwright_with_context_and_video(
    start_url: str,
    browsertype: str,
    headless: Optional[bool] = False,
    stealthmode: Optional[bool] = True,
    user_data_dir: Optional[
        str
    ] = None,  # Optional parameter to pass saved cookies
) -> Tuple[Playwright, Page, Video]:
    """Creates a Playwright browser, opens a new page, and navigates to a
    specified URL.

    Important, call playwright.stop() once you are done.

    Returns:
        tuple[Browser, Page]: A tuple containing the browser and page objects.
    """
    width: int = 1280
    height: int = 720
    padding: int = 10
    page: Page
    browser: BrowserContext
    playwright: Playwright = sync_playwright().start()
    if browsertype == "firefox":
        browser = playwright.firefox.launch_persistent_context(
            user_data_dir=user_data_dir, headless=headless
        )
    if browsertype == "chromium":
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=headless,
            viewport={"width": width + padding, "height": height + padding},
            record_video_dir="./",
            record_video_size={
                "width": width + padding,
                "height": height + padding,
            },
        )
    if browsertype == "safari":
        raise NotImplementedError("Error, did not implement webkit launch.")
    # context = browser.new_context(

    #     )

    if len(browser.pages) == 0:
        page = browser.new_page()
    else:
        page = browser.pages[0]

    if stealthmode:
        stealth_sync(page)

        # page = context.new_page()

    video: Video = page.video

    page.goto(start_url)
    return playwright, page, video


@typechecked
def get_page(
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

    return playwright, page
