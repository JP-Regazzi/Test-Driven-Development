import time
from playwright.sync_api import Page, expect
from Pages.base_page import BasePage

class EmployeeDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
    def employee_details (self, last_name, first_name, birthday):
        page = self.page
        page.get_by_role("link", name="PIM").click()
        self.get_by_label( 'Employee Name').click()
        time.sleep(0.2)
        self.get_by_label( 'Employee Name').type(last_name)
        time.sleep(0.2)
        page.get_by_role("button", name="Search").click()
        page.locator("div.orangehrm-employee-list").locator("div[role='rowgroup']").nth(1).locator(
            "div[role='cell']").nth(2).click()
        expect(page.get_by_text(f"{first_name} {last_name}")).to_be_visible()
        page.locator("xpath=//label[text()='Nationality']/../..//i").click()
        page.locator("div[role='listbox']").get_by_text("French").click()
        page.locator("xpath=//label[text()='Marital Status']/../..//i").click()
        page.locator("div[role='listbox']").get_by_text("Single").click()
        date_of_birth = page.locator("xpath=//label[text()='Date of Birth']/../..").get_by_placeholder("yyyy-dd-mm")
        date_of_birth.fill(birthday)
        page.locator("xpath=//label[text()='Male']").click()
        page.get_by_role("button", name="Save").nth(0).click()

