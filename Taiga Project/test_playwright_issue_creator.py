import pytest
from unittest.mock import Mock
from playwright_issue_creator import login, go_to_issues_page, create_issues_from_csv

@pytest.fixture
def mock_page():
    return Mock()

def test_login(mock_page):
    login(mock_page, "user", "pass")
    mock_page.goto.assert_called_with("https://tree.taiga.io/login")
    mock_page.fill.assert_any_call("input[name='username']", "user")
    mock_page.fill.assert_any_call("input[name='password']", "pass")
    mock_page.click.assert_called_with("button[type='submit']")

def test_go_to_issues_page(mock_page):
    go_to_issues_page(mock_page, "slug")
    mock_page.goto.assert_called_with("https://tree.taiga.io/project/slug/issues")

def test_create_issues_from_csv(monkeypatch, mock_page, tmp_path):
    csv_path = tmp_path / "issues.csv"
    csv_path.write_text("subject,description,priority,severity,status,type\nBug,Desc,4973875,8280271,11599427,4984469", encoding="utf-8")
    mappings = {
        "priority": {"4973875": 2},
        "severity": {"8280271": 3},
        "status": {"11599427": 3},
        "type": {"4984469": 1}
    }

    create_issues_from_csv(mock_page, str(csv_path), mappings)
    mock_page.fill.assert_any_call("input[name='subject']", "Bug")
    mock_page.fill.assert_any_call("textarea[name='description']", "Desc")
    assert mock_page.click.call_count > 0
