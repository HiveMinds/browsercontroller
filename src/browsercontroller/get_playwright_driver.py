"""Gets the Playwright website controller and opens it. Prerequisites: pip
install pytest-playwright playwright install.

(Or with anaconda:) conda config --add channels conda-forge conda config
--add channels microsoft conda install playwright
"""

from typing import Optional

from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Browser, Locator, Page
from typeguard import typechecked


@typechecked
def has_conversation_id(*, page: Page, turn_nr: int) -> bool:
    """Returns whether a conversation turn with nr <number> is found."""

    element = page.locator(f'[data-testid="conversation-turn-{turn_nr}"]')
    if element.count() > 0:
        return True
    return False


def get_chatgpt_conversation(*, page: Page, turn_nr: int) -> str:
    """Gets the HTML content of an element with a specified data-testid
    attribute.

    Args:
        page (Page): The Playwright Page object.
        test_id (str): The value of the data-testid attribute to locate the
        element.

    Returns:
        str: The HTML content of the element, or an empty string if not found.
    """
    element = page.locator(f'[data-testid="conversation-turn-{turn_nr}"]')
    if element.count() > 0:
        return element.inner_html()
    raise ValueError(f"Error, expected to find conversation turn:{turn_nr}")


@typechecked
def fill_in_question_input_form(*, page: Page, text: str) -> Locator:
    """Enters text into a textarea field.

    Args:
        page (Page): The Playwright Page object.
        text (str): The text to be entered into the textarea.

    Returns:
        None
    """
    textarea: Locator = page.locator("textarea#prompt-textarea")
    textarea.fill(text)
    return textarea


def click_button_by_text(*, page: Page, text: str) -> bool:
    """Clicks on a button with the specified text.

    Args:
        page (Page): The Playwright Page object.
        text (str): The text content of the button to click.

    Returns:
        bool: True if the button was found and clicked, False otherwise.
    """
    button_selector: str = f'//div[contains(text(), "{text}")]'
    button: Locator = page.locator(button_selector)
    if button.count() > 0:
        button.click()
        return True
    return False


def find_element_with_text(
    page: Page,
    text: str,
    strict: bool = True,
    element_type: Optional[str] = None,
) -> Locator:
    """Find a Playwright element containing the specified text on the page.

    Args:
        page (Page): The Playwright page to search on.
        text (str): The text to search for in the element.
        strict (bool): Whether to perform a strict search. If True, the text
        must match exactly. Defaults to True.

    Returns:
        Locator: A Playwright Locator object representing the found element.

    Raises:
        Exception: If the element with the specified text is not found.

    Example:
        element = find_element_with_text(page, "Email address")
    """
    locator: Locator
    if element_type:
        if not is_valid_element_type(element_type=element_type):
            raise ValueError("Error: Invalid element type.")
        locator = get_element_by_name_in_html(
            text_content=text, element_type=element_type, page=page
        )
    else:
        if strict:
            locator = page.locator(
                f"//{strict and '' or '*'}[contains(text(), '{text}')]"
            )
        else:
            locator = page.locator(text)
    print(f"The element has text:{locator.text_content()}")
    return locator


@typechecked
def is_in_cloudfare(*, page: Page) -> bool:
    """Returns true if the website contains cloudfare and or "are you
    human"."""
    # Get the page content
    page_content: str = page.content()

    # Check if the words "swag" or "banana" are present
    if (
        "cloudfare" in page_content.lower()
        or "you are human" in page_content.lower()
        or "challenge-form" in page_content.lower()
    ):
        return True
    if "https://chat.openai.com/api/auth/error" in page.url:
        return True
    return False


@typechecked
def is_valid_element_type(*, element_type: str) -> bool:
    """Verifies if the given element type is a valid HTML element type.

    a: Represents a hyperlink (anchor) element.
    button: Represents a clickable button element.
    div: Represents a division or container element.
    span: Represents an inline container for text or other inline elements.
    input: Represents an input field, which can be of various types (e.g.,
    text, password, checkbox).
    textarea: Represents a multiline text input field.
    select: Represents a dropdown list or select box.
    ul: Represents an unordered list.
    ol: Represents an ordered (numbered) list.
    li: Represents a list item within an ordered or unordered list.
    table: Represents a data table.
    tr: Represents a table row.
    td: Represents a table cell.
    th: Represents a table header cell.
    form: Represents an HTML form.
    label: Represents a label for an input element.
    img: Represents an image element.
    h1, h2, h3, h4, h5, h6: Represents heading elements of different levels.
    p: Represents a paragraph element.
    iframe: Represents an inline frame for embedding another document.
    nav: Represents a navigation element.
    footer: Represents a footer element often used for copyright or contact
    information.
    header: Represents a header element, typically containing site branding or
      navigation links.
    section: Represents a section or thematic grouping of content.
    article: Represents an article or self-contained piece of content.
    aside: Represents content that is tangentially related to the content
    around it.
    blockquote: Represents a block of text that is a quotation from another
    source.

    Args:
        element_type (str): The element type to be checked.

    Returns:
        bool: True if the element type is valid, False otherwise.
    """
    valid_element_types = [
        "a",
        "button",
        "div",
        "span",
        "input",
        "textarea",
        "select",
        "ul",
        "ol",
        "li",
        "table",
        "tr",
        "td",
        "th",
        "form",
        "label",
        "img",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "p",
        "iframe",
        "nav",
        "footer",
        "header",
        "section",
        "article",
        "aside",
        "blockquote",
    ]

    return element_type.lower() in valid_element_types


@typechecked
def get_element_by_name_in_html(
    *,
    text_content: str,
    element_type: str,
    page: Page,
) -> Locator:
    """Locates and clicks an element on the page based on its text content and
    element type.

    Args:
        page (Page): The Playwright page object.
        element_type (str): The type of element to search for.
        text_content (str): The text content to search for (case-insensitive).

    Returns:
        page element.
    """

    if not is_valid_element_type(element_type=element_type):
        raise ValueError("Error: Invalid element type.")
    # Construct an XPath expression to find the element by its text content

    xpath_expression: str = (
        f'//{element_type}[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ",'
        + f' "abcdefghijklmnopqrstuvwxyz"), "{text_content}")]'
    )

    # Locate the element based on the XPath expression
    element = page.locator(xpath_expression)

    print(f"The element has text:{element.text_content()}")
    return element


@typechecked
def get_element_by_xpath_in_html(
    *,
    some_xpath: str,
    page: Page,
) -> Locator:
    """Returns an object that you can click based on a name in the html string
    of that object."""
    some_button: Locator = page.locator(some_xpath)
    return some_button


@typechecked
def initialise_playwright_browsercontroller(
    start_url: str,
) -> tuple[Browser, Page]:
    """
    Creates a Playwright browser, opens a new page, and navigates to a
    specified URL.
    TODO: allow returning the object within the with statement and using it
    outside this function.

    Returns:
        tuple[Browser, Page]: A tuple containing the browser and page objects.
    """
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            if (
                browser_type.name != "webkit"
                and browser_type.name == "firefox"
            ):
                print(f"browser_type={browser_type.name}")
                browser = browser_type.launch()

                # Create a new page and navigate to the URL
                # url = "https://chat.openai.com/auth/login"
                page = browser.new_page()
                page.goto(start_url)

                # Return the browser and page objects
                return browser, page
    raise ValueError("Error: Could not find browser.")
