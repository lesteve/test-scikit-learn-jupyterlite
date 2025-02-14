import pytest
import time

from playwright.sync_api import expect


@pytest.mark.parametrize(
    "url",
    [
        "https://scikit-learn.org/stable/lite/lab/index.html",
        "https://scikit-learn.org/dev/lite/lab/index.html",
    ],
)
def test_pyodide_kernel(page, url):
    page.goto(url)
    page.get_by_text("Python (Pyodide)").first.click()
    page.get_by_role("textbox").locator("div").click()
    page.keyboard.type('(20 + 25) ** 2')
    page.keyboard.press("Shift+Enter")
    expect(page.get_by_text("2025", exact=True)).to_be_visible(timeout=30_000)
    page.keyboard.type('print("kernel ready")')
    page.keyboard.press("Shift+Enter")
    expect(page.get_by_text("kernel ready", exact=True)).to_be_visible(timeout=30_000)
