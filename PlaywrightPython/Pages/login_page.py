from playwright.sync_api import Page, expect
from Pages.base_page import BasePage

class LoginPage (BasePage):
    def __init__(self, page):
        super().__init__(page)

    def login(self, username, password):
        page= self.page
        page.goto(self.base_url)
        page.get_by_role("textbox", name="Username").fill(username)
        page.get_by_role("textbox", name="Password").fill(password)
        page.get_by_role("button", name="Login").click()

    def check_pim_menu(self):
        page = self.page
        expect(page.locator("a[href*='/pim/viewPimModule']")).to_have_text("PIM")

    def username_visible(self):
        page = self.page
        expect (page.get_by_role("textbox", name="Username")).to_be_visible()

