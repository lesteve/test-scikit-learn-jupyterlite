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
    max_attempts = 10
    for n_attempt in range(max_attempts):
        try:
            page.goto(url)
            page.get_by_text("Python (Pyodide)").first.click()
            break
        except TimeoutError:
            print(f"failure on attempt {n_attempt}")
            time.sleep(5)
            if n_attempt == max_attempt - 1:
                raise

    time.sleep(5)
    page.get_by_role("textbox").locator("div").click()
    page.keyboard.type("(20 + 25) ** 2")
    page.keyboard.press("Shift+Enter")
    expect(page.get_by_text("2025", exact=True)).to_be_visible(timeout=30_000)
    page.keyboard.type('print("kernel ready")')
    page.keyboard.press("Shift+Enter")
    expect(page.get_by_text("kernel ready", exact=True)).to_be_visible(timeout=30_000)
