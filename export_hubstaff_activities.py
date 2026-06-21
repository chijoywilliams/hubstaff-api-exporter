import json
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import pandas as pd

from hubstaff_auth import hubstaff_get


API_BASE = "https://api.hubstaff.com/v2"


def normalize_response(data):
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                return value
        return [data]

    return []


def get_first_organization_id():
    org_data = hubstaff_get(f"{API_BASE}/organizations")

    if isinstance(org_data, dict):
        for value in org_data.values():
            if isinstance(value, list) and value:
                return value[0]["id"]

    if isinstance(org_data, list) and org_data:
        return org_data[0]["id"]

    raise RuntimeError("No organization found.")


def main():
    organization_id = get_first_organization_id()

    stop_time = datetime.now(timezone.utc)
    start_time = stop_time - timedelta(days=7)

    params = {
        "time_slot[start]": start_time.isoformat().replace("+00:00", "Z"),
        "time_slot[stop]": stop_time.isoformat().replace("+00:00", "Z"),
        "page_limit": 100,
    }

    url = f"{API_BASE}/organizations/{organization_id}/activities?{urlencode(params)}"

    print(f"Organization ID: {organization_id}")
    print(f"Calling: {url}")

    data = hubstaff_get(url)

    print("Raw response:")
    print(json.dumps(data, indent=2))

    rows = normalize_response(data)

    if not rows:
        print("No activity rows found.")
        print("This is normal if you have not tracked time yet.")
        pd.DataFrame().to_csv("hubstaff_activities.csv", index=False)
        print("Saved empty file: hubstaff_activities.csv")
        return

    df = pd.json_normalize(rows)
    df.to_csv("hubstaff_activities.csv", index=False)

    print("Saved: hubstaff_activities.csv")
    print(df.head())


if __name__ == "__main__":
    main()
