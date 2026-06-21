import json
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
    url = f"{API_BASE}/organizations/{organization_id}/projects"

    print(f"Organization ID: {organization_id}")
    print(f"Calling: {url}")

    data = hubstaff_get(url)

    print("Raw response:")
    print(json.dumps(data, indent=2))

    rows = normalize_response(data)

    if not rows:
        print("No project rows found.")
        return

    df = pd.json_normalize(rows)
    df.to_csv("hubstaff_projects.csv", index=False)

    print("Saved: hubstaff_projects.csv")
    print(df.head())


if __name__ == "__main__":
    main()
