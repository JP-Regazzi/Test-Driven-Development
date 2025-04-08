import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from generate_anomalies_from_csv import read_csv, create_issue, create_issues_from_csv

def test_read_csv():
    csv_content = "subject,description,priority,severity,status,type\nBug A,Desc A,1,2,3,4"
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', newline='') as f:
        f.write(csv_content)
        temp_path = f.name

    rows = read_csv(temp_path)
    assert len(rows) == 1
    assert rows[0]["subject"] == "Bug A"
    os.remove(temp_path)
    print("✅ test_read_csv passed")

@patch("generate_anomalies_from_csv.requests.post")
def test_create_issue(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response

    row = {
        "subject": "Bug A",
        "description": "Desc A",
        "priority": "1",
        "severity": "2",
        "status": "3",
        "type": "4"
    }
    response = create_issue(row, 12345, "fake_token")
    assert response.status_code == 201
    mock_post.assert_called_once()
    print("✅ test_create_issue passed")

@patch("generate_anomalies_from_csv.requests.post")
def test_create_issues_from_csv(mock_post, tmp_path):
    csv_content = "subject,description,priority,severity,status,type\nBug A,Desc A,1,2,3,4"
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(csv_content, encoding="utf-8")

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "project": 1656687,
        "subject": "Bug A",
        "description": "Desc A",
        "id": 123,
        "created_date": "2025-04-08T13:07:15.908Z",
        "status": 3
    }
    mock_post.return_value = mock_response

    create_issues_from_csv(str(csv_path), 1656687, "fake_token")
    assert mock_post.call_count == 1
    print("✅ test_create_issues_from_csv passed")
