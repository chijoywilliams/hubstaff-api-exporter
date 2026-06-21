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


def main():
    url = f"{API_BASE}/organizations"

    print(f"Calling: {url}")
    data = hubstaff_get(url)

    print("Raw response:")
    print(json.dumps(data, indent=2))

    rows = normalize_response(data)

    if not rows:
        print("No organization rows found.")
        return

    df = pd.json_normalize(rows)
    df.to_csv("hubstaff_organizations.csv", index=False)

    print("Saved: hubstaff_organizations.csv")
    print(df.head())


if __name__ == "__main__":
    main()
