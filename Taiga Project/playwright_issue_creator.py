import argparse
import csv
import time
from playwright.sync_api import sync_playwright

def login(page, username, password):
    print("Navigating to the Taiga login page...")
    page.goto("https://tree.taiga.io/login")
    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

def go_to_issues_page(page, project_slug):
    issues_url = f"https://tree.taiga.io/project/{project_slug}/issues"
    print(f"Navigating directly to issues page: {issues_url}")
    page.goto(issues_url)
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    try:
        page.click("xpath=/html/body/cookie-warning/div/a", timeout=2000)
        print("Cookie warning closed.")
    except:
        print("Cookie warning not present or already closed, proceeding...")

def create_issues_from_csv(page, csv_path, mappings):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            subject = row["subject"]
            print(f"Creating issue: {subject}")

            page.click("text=New issue")
            time.sleep(1)

            page.fill("input[name='subject']", row["subject"])
            page.fill("textarea[name='description']", row["description"])
            time.sleep(0.5)

            prio_idx = mappings["priority"].get(row["priority"], 2)
            page.click("xpath=/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-priority-button/div")
            prio_xpath = f"/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-priority-button/div/ul/li[{prio_idx}]/a"
            page.click(f"xpath={prio_xpath}")
            time.sleep(0.5)

            sev_idx = mappings["severity"].get(row["severity"], 3)
            page.click("xpath=/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-severity-button/div")
            sev_xpath = f"/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-severity-button/div/ul/li[{sev_idx}]/a/span"
            page.click(f"xpath={sev_xpath}")
            time.sleep(0.5)

            status_idx = mappings["status"].get(row["status"], 1)
            page.click("xpath=/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/fieldset/div")
            if status_idx in [1, 7]:
                status_xpath = f"/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/fieldset/ul/li[{status_idx}]/a"
            else:
                status_xpath = f"/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/fieldset/ul/li[{status_idx}]/a/span"
            page.click(f"xpath={status_xpath}")
            time.sleep(0.5)

            type_idx = mappings["type"].get(row["type"], 1)
            page.click("xpath=/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-type-button/div")
            type_xpath = f"/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-type-button/div/ul/li[{type_idx}]/a/span"
            page.click(f"xpath={type_xpath}")
            time.sleep(0.5)

            page.click("xpath=//*[@id='submitButton']")
            page.wait_for_load_state("networkidle")
            time.sleep(2)
            print(f"Issue '{subject}' created.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", type=str, required=True)
    parser.add_argument("--password", type=str, required=True)
    parser.add_argument("--project_slug", type=str, default="jp_regazzi-tdd-project")
    parser.add_argument("--csv", type=str, default="anomalies.csv")
    args = parser.parse_args()

    mappings = {
        "priority": {"4973874": 1, "4973875": 2, "4973876": 3},
        "severity": {"8280269": 1, "8280270": 2, "8280271": 3, "8280272": 4, "8280273": 5},
        "status": {"11599425": 1, "11599426": 2, "11599427": 3, "11599428": 4, "11599429": 5, "11599430": 6, "11599431": 7},
        "type": {"4984469": 1, "4984470": 2, "4984471": 3}
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        login(page, args.username, args.password)
        go_to_issues_page(page, args.project_slug)
        create_issues_from_csv(page, args.csv, mappings)

        context.close()
        browser.close()

if __name__ == "__main__":
    main()


# # Priority options:
#     priority_option = {
#         "4973874": 1, # Low
#         "4973875": 2, # Normal
#         "4973876": 3 # High
#     }
#     # Severity options:
#     severity_option = {
#         "8280269": 1, # Wishlist
#         "8280270": 2, # Minor
#         "8280271": 3, # Normal
#         "8280272": 4, # Important
#         "8280273": 5 # Critical
#     }
#     # Status options:
#     status_option = {
#         "11599425": 1, # New
#         "11599426": 2, # In progress
#         "11599427": 3, # Ready for test
#         "11599428": 4, # Closed
#         "11599429": 5, # Needs Info
#         "11599430": 6, # Rejected
#         "11599431": 7 # Postponed
#     }
#     # Type options:
#     type_option = {
#         "4984469": 1, # Bug
#         "4984470": 2, # Question
#         "4984471": 3 # Enhancement
#     }