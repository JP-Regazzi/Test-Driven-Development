import sys
import os
import pytest
import Pages

from playwright.sync_api import Page
import pytest


@pytest.mark.skip(reason="Debug")
def test_login_logout(page: Page):
    p_login = Pages.LoginPage(page)
    p_login.login("Admin", "admin123")
    p_login.check_pim_menu()
    p_add = Pages.AddEmployeePage(page)
    p_add.add_employee()
    p_home = Pages.BasePage(page)
    p_home.logout()
    p_login.username_visible()

@pytest.mark.skip(reason="Debug")
def test_add_employee (page:Page, auth):
    page = auth.new_page()
    p = Pages.AddEmployeePage(page)
    page.close()
def test_search_employee (page:Page, auth):
    page = auth.new_page()
    p_list = Pages.EmployeeListPage(page)
    p_list.search_employee_by_name("Russel")
    p_list.check_cell_content(1, 2, "Russel")
    page.close()

@pytest.mark.skip(reason="Debug")
def test_employee_details (page:Page, auth):
    page = auth.new_page()
    p = Pages.EmployeeDetailsPage(page)
    page.close()

