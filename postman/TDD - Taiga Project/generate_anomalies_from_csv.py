import argparse
import csv
import requests

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Create Taiga issues from a CSV file.")
    parser.add_argument("-id", "--project_id", type=int, default=1656687,
                        help="Project ID to use (default: 1656687)")
    parser.add_argument("-t", "--token", type=str,
                        default=("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9."
                                 "eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MDcwNjM1LCJqdGkiOiIwMzU4YTBjYmE5YjM0MzI0Yjk2ZDBlODcxNTZkZmRmMyIsInVzZXJfaWQiOjc3NTUxNn0."
                                 "fsW7II-Vmr_b44xGqs_yPrQm3oflF2t1L6tSm4r4xo56p3PfgXKvVnwha_-vrA97mZeaEy1Foe8KW1pII5KzjJatNeeOHSHsQC4HpqQavO0qEZzTC5tRJkyXyaVq5KQp1vN4BvpAtkeKhCNMin9r7xkItGLGW6w-FEHbPmtSZMI-9y7LEx2u95hFONCkMH4f8nzDejFHOyxeOzLAjjcrLJiZo2lWrGwBdhLbkwo-faPacI07osprAQ4BOptsLKZNq168kZvnL8TNAN1WeeLGbZib3POL7mtWBPvdn7Fdc1MTEq31CwPHKBCpEC9N-WSv3QYpA6rGgCpleET_M1hiWg"),
                        help="Auth token (do not include 'Bearer ' - it is added automatically)")
    parser.add_argument("--csv", type=str, default="anomalies.csv",
                        help="Path to CSV file with anomalies (default: anomalies.csv)")
    
    args = parser.parse_args()

    # Prepare the header with the token
    headers = {
        "Authorization": f"Bearer {args.token}",
        "Content-Type": "application/json"
    }
    url = "https://api.taiga.io/api/v1/issues"
    
    # Process CSV file and create issues
    with open(args.csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            payload = {
                "project": args.project_id,
                "subject": row["subject"],
                "description": row["description"],
                "priority": int(row["priority"]),
                "severity": int(row["severity"]),
                "status": int(row["status"]),
                "type": int(row["type"])
            }
    
            response = requests.post(url, headers=headers, json=payload)
    
            if response.status_code == 201:
                print(f"✅ Created: {row['subject']}")
            else:
                print(f"❌ Error for {row['subject']}: {response.status_code} - {response.text}")
    
if __name__ == "__main__":
    main()
