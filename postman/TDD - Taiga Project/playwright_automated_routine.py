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
    
    # Mapping dictionaries (for display or fallback purposes)
    priority_map = {
        "4973874": "Low",        # Easy
        "4973875": "Normal",     # Medium
        "4973876": "High"        # Hard
    }
    severity_map = {
        "8280269": "Wishlist",   # Option 1 (if needed)
        "8280270": "Minor",      # Option 2
        "8280271": "Normal",     # Option 3
        "8280272": "Important",  # Option 4
        "8280273": "Critical"    # Option 5
    }
    status_map = {
        "11599425": "New",
        "11599426": "In progress",
        "11599427": "Ready for test",
        "11599428": "Closed",
        "11599429": "Needs Info",
        "11599430": "Rejected",
        "11599431": "Postponed"
    }
    type_map = {
        "4984469": "Bug",
        "4984470": "Question",
        "4984471": "Enhancement"
    }
    
    # Option number mappings for XPath selection:
    # Priority options:
    #   Low    -> li[1]
    #   Normal -> li[2]
    #   High   -> li[3]
    priority_option = {
        "4973874": 1,
        "4973875": 2,
        "4973876": 3
    }
    # Severity options:
    #   Wishlist -> li[1] (if used)
    #   Minor    -> li[2]
    #   Normal   -> li[3]
    #   Important-> li[4]
    #   Critical -> li[5]
    severity_option = {
        "8280269": 1,
        "8280270": 2,
        "8280271": 3,
        "8280272": 4,
        "8280273": 5
    }
    # Status options:
    #   New         -> li[1] (XPath ending with /a)
    #   In progress -> li[2] (/a/span)
    #   Ready for test -> li[3] (/a/span)
    #   Closed      -> li[4] (/a/span)
    #   Needs Info  -> li[5] (/a/span)
    #   Rejected    -> li[6] (/a/span)
    #   Postponed   -> li[7] (/a)
    status_option = {
        "11599425": 1,
        "11599426": 2,
        "11599427": 3,
        "11599428": 4,
        "11599429": 5,
        "11599430": 6,
        "11599431": 7
    }
    # Type options:
    #   Bug         -> li[1]
    #   Question    -> li[2]
    #   Enhancement -> li[3]
    type_option = {
        "4984469": 1,
        "4984470": 2,
        "4984471": 3
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
                prio_idx = priority_option.get(row["priority"], 2)
                prio_xpath = f"/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-priority-button/div/ul/li[{prio_idx}]/a"
                page.click(f"xpath={prio_xpath}")
                time.sleep(0.5)

                # --- Select Severity using full XPath ---
                # Open severity menu:
                page.click("xpath=/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-severity-button/div")
                time.sleep(0.5)
                sev_idx = severity_option.get(row["severity"], 3)
                sev_xpath = f"/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/div/div/div[1]/tg-issue-severity-button/div/ul/li[{sev_idx}]/a/span"
                page.click(f"xpath={sev_xpath}")
                time.sleep(0.5)

                # --- Select Status using full XPath ---
                page.click("xpath=/html/body/div[2]/div/div/div[1]/form/div[2]/div[1]/sidebar/fieldset/div")
                time.sleep(0.5)
                status_idx = status_option.get(row["status"], 1)
                # For "New" (idx=1) and "Postponed" (idx=7) use /a, others use /a/span
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
