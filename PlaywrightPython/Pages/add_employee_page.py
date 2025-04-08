import time
from playwright.sync_api import Page, expect
from .base_page import BasePage
from .providers import Employee

class AddEmployeePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
    def add_employee(self):
        page = self.page
        self.emp = Employee.fake_employee()
        page.goto(f"{self.base_url}/web/index.php/dashboard/index")
        page.get_by_role("link", name="PIM").click()
        page.get_by_role("button", name="Add").click()
        page.get_by_role("textbox", name="First Name").fill(self.emp.first_name)
        page.get_by_role("textbox", name="Last Name").fill(self.emp.last_name)
        self.get_by_label('Employee Id').fill(self.emp.id)
        page.get_by_role("button", name="Save").click()
        expect(page.get_by_text(f"{self.emp.first_name} {self.emp.last_name}")).to_be_visible()

    def employee_details (self, last_name, first_name):
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
        date_of_birth.fill(self.emp.birthday)
        page.locator("xpath=//label[text()='Male']").click()
        page.get_by_role("button", name="Save").nth(0).click()

