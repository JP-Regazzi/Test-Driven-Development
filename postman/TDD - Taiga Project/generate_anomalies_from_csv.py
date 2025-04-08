import csv
import requests
import argparse

def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

def create_issue(row, project_id, token):
    url = "https://api.taiga.io/api/v1/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "project": project_id,
        "subject": row["subject"],
        "description": row["description"],
        "priority": int(row["priority"]),
        "severity": int(row["severity"]),
        "status": int(row["status"]),
        "type": int(row["type"])
    }
    return requests.post(url, headers=headers, json=payload)

def create_issues_from_csv(file_path, project_id, token):
    rows = read_csv(file_path)
    for row in rows:
        response = create_issue(row, project_id, token)

        if response.status_code == 201:
            try:
                data = response.json()

                # Basic field checks
                assert data.get("project") == project_id, f"Project ID mismatch: {data.get('project')} != {project_id}"
                assert data.get("subject") == row["subject"], f"Subject mismatch: {data.get('subject')} != {row['subject']}"
                assert data.get("description") == row["description"], f"Description mismatch: {data.get('description')} != {row['description']}"
                assert isinstance(data.get("id"), int), "Missing or invalid issue ID"
                assert "created_date" in data, "Missing created_date"
                assert data.get("status") == int(row["status"]), f"Status mismatch: {data.get('status')} != {row['status']}"

                print(f"✅ Created: {row['subject']} (ID: {data['id']})")

            except Exception as e:
                print(f"⚠️ Created but validation failed for {row['subject']}: {e}")

        else:
            print(f"❌ Error for {row['subject']}: {response.status_code} - {response.text}")


def main():
    parser = argparse.ArgumentParser(description="Create Taiga issues from a CSV file.")
    parser.add_argument("-id", "--project_id", type=int, default=1656687,
                        help="Project ID to use (default: 1656687)")
    parser.add_argument("-t", "--token", type=str,
                        help="Auth token (without 'Bearer ')")
    parser.add_argument("--csv", type=str, default="anomalies.csv",
                        help="Path to the anomalies CSV file (default: anomalies.csv)")

    args = parser.parse_args()
    create_issues_from_csv(args.csv, args.project_id, args.token)


if __name__ == "__main__":
    main()
