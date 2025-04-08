import time
from playwright.sync_api import Page, expect
from Pages.base_page import BasePage

class EmployeeListPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def search_employee_by_name(self, last_name):
        page = self.page
        page.goto(f"{self.base_url}/web/index.php/dashboard/index")
        page.get_by_role("link", name="PIM").click()
        self.get_by_label('Employee Name').click()
        time.sleep(0.2)
        self.get_by_label('Employee Name').type(last_name)
        time.sleep(0.2)
        page.get_by_role("button", name="Search").click()
    def check_cell_content (self, row, column, value):
        page = self.page
        cell = self.get_cell ("div.orangehrm-employee-list", row, column)
        expect(cell).to_have_text(value)

