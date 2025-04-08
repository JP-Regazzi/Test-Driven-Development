import pytest
from playwright.sync_api import Browser, BrowserContext, expect
@pytest.fixture(scope="module")
def auth(browser: Browser, request):
    base_url = request.config.getoption("--base-url")
    context = browser.new_context(viewport={ 'width': 1920, 'height': 1090 })
    page = context.new_page()
    # SETUP : Login
    page.goto(base_url)
    page.get_by_role("textbox", name="Username").fill("Admin")
    page.get_by_role("textbox", name="Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    expect (page.locator("a[href*='/pim/viewPimModule']")).to_have_text("PIM")

    yield context  # Exécution des tests

    # TEARDOWN : Logout
    page.locator("p.oxd-userdropdown-name").click()
    page.get_by_role("menuitem", name="Logout").click()
    context.close()
