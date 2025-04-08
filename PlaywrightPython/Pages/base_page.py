from playwright.sync_api import Page

class BasePage:
    def __init__(self, page):
        self.page = page
        self.base_url = "https://opensource-demo.orangehrmlive.com"

    def logout (self):
        page= self.page
        page.locator("p.oxd-userdropdown-name").click()
        page.get_by_role("menuitem", name="Logout").click()

    def get_by_label(self, label):
        page= self.page
        element = page.locator(f"xpath=//label[text()='{label}']/../..//input")
        return (element)

    def get_cell(self, table_locator, row, column):
        page= self.page
        row = page.locator(table_locator).locator("div[role='row']").nth(row)
        cell = row.locator("div[role='cell']").nth(column)
        return (cell)
