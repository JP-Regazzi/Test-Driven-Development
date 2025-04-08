import argparse
import csv
import time
from playwright.sync_api import sync_playwright

def main():
    parser = argparse.ArgumentParser(
        description="Create Taiga issues from a CSV file using Playwright with full XPath selectors."
    )
    parser.add_argument("--username", type=str, default="YOUR_USERNAME",
                        help="Your Taiga username/email (default: YOUR_USERNAME)")
    parser.add_argument("--password", type=str, default="YOUR_PASSWORD",
                        help="Your Taiga password (default: YOUR_PASSWORD)")
    parser.add_argument("--project_slug", type=str, default="jp_regazzi-tdd-project",
                        help="Your project slug from the Taiga URL (default: jp_regazzi-tdd-project)")
    parser.add_argument("--csv", type=str, default="anomalies.csv",
                        help="Path to the anomalies CSV file (default: anomalies.csv)")
    
    args = parser.parse_args()
    
    # Option number mappings for XPath selection:
    # Priority options:
    priority_option = {
        "4973874": 1, # Low
        "4973875": 2, # Normal
        "4973876": 3 # High
    }
    # Severity options:
    severity_option = {
        "8280269": 1, # Wishlist
        "8280270": 2, # Minor
        "8280271": 3, # Normal
        "8280272": 4, # Important
        "8280273": 5 # Critical
    }
    # Status options:
    status_option = {
        "11599425": 1, # New
        "11599426": 2, # In progress
        "11599427": 3, # Ready for test
        "11599428": 4, # Closed
        "11599429": 5, # Needs Info
        "11599430": 6, # Rejected
        "11599431": 7 # Postponed
    }
    # Type options:
    type_option = {
        "4984469": 1, # Bug
        "4984470": 2, # Question
        "4984471": 3 # Enhancement
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 1. Log in to Taiga.
        print("Navigating to the Taiga login page...")
        page.goto("https://tree.taiga.io/login")
        page.fill("input[name='username']", args.username)
        page.fill("input[name='password']", args.password)
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        # 2. Navigate directly to the project's Issues page.
        issues_url = f"https://tree.taiga.io/project/{args.project_slug}/issues"
        print(f"Navigating directly to issues page: {issues_url}")
        page.goto(issues_url)
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        # Attempt to close the cookies warning if present
        try:
            page.click("xpath=/html/body/cookie-warning/div/a", timeout=2000)
            print("Cookie warning closed.")
        except Exception as e:
            print("Cookie warning not present or already closed, proceeding...")

        # 3. Read the CSV file and create issues.
        print(f"Reading CSV file: {args.csv}")
        with open(args.csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                subject = row["subject"]
                print(f"Creating issue: {subject}")

                # Click "New issue" to open the creation form.
                page.click("text=New issue")
                time.sleep(1)

                # Fill Subject and Description
                page.fill("input[name='subject']", row["subject"])
                page.fill("textarea[name='description']", row["description"])
                time.sleep(0.5)

                # --- Select Priority using full XPath ---
                # Open priority menu:
                page.click("xpath=/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-priority-button/div")
                time.sleep(0.5)
                # Select priority:
                prio_idx = priority_option.get(row["priority"], 2)
                prio_xpath = f"/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-priority-button/div/ul/li[{prio_idx}]/a"
                page.click(f"xpath={prio_xpath}")
                time.sleep(0.5)

                # --- Select Severity using full XPath ---
                # Open severity menu:
                page.click("xpath=/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-severity-button/div")
                time.sleep(0.5)
                # select severiy:
                sev_idx = severity_option.get(row["severity"], 3)
                sev_xpath = f"/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-severity-button/div/ul/li[{sev_idx}]/a/span"
                page.click(f"xpath={sev_xpath}")
                time.sleep(0.5)

                # --- Select Status using full XPath ---
                # Open status menu:
                page.click("xpath=/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/fieldset/div")
                time.sleep(0.5)
                # Select status:
                status_idx = status_option.get(row["status"], 1)
                # OBS: "New" (idx=1) and "Postponed" (idx=7) use /a, others use /a/span
                if status_idx == 1 or status_idx == 7:
                    status_xpath = f"/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/fieldset/ul/li[{status_idx}]/a"
                else:
                    status_xpath = f"/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/fieldset/ul/li[{status_idx}]/a/span"
                page.click(f"xpath={status_xpath}")
                time.sleep(0.5)

                # --- Select Type using full XPath ---
                page.click("xpath=/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-type-button/div")
                time.sleep(0.5)
                type_idx = type_option.get(row["type"], 1)
                type_xpath = f"/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-type-button/div/ul/li[{type_idx}]/a/span"
                page.click(f"xpath={type_xpath}")
                time.sleep(0.5)

                # --- Create the Issue by clicking the copy/submit button ---
                page.click("xpath=//*[@id='submitButton']")
                page.wait_for_load_state("networkidle")
                time.sleep(2)
                print(f"Issue '{subject}' created.")

        print("All issues processed. Closing browser.")
        context.close()
        browser.close()

if __name__ == "__main__":
    main()


#python .\playwright_automated_routine.py --username email --password password