from pathlib import Path
import csv


EXPORT_FILES = [
    "hubstaff_organizations.csv",
    "hubstaff_projects.csv",
    "hubstaff_members.csv",
    "hubstaff_activities.csv",
]


def inspect_csv(file_path):
    path = Path(file_path)

    if not path.exists():
        return {
            "file": file_path,
            "status": "missing",
            "rows": 0,
            "columns": 0,
            "sample_columns": "",
        }

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = list(csv.reader(file))

    if not reader:
        return {
            "file": file_path,
            "status": "empty",
            "rows": 0,
            "columns": 0,
            "sample_columns": "",
        }

    header = reader[0]
    data_rows = [row for row in reader[1:] if any(cell.strip() for cell in row)]

    return {
        "file": file_path,
        "status": "available",
        "rows": len(data_rows),
        "columns": len(header),
        "sample_columns": ", ".join(header[:6]),
    }


def main():
    results = [inspect_csv(file_name) for file_name in EXPORT_FILES]

    print("Hubstaff Export Summary")
    print("=" * 80)

    for result in results:
        print(
            f"{result['file']}: "
            f"{result['status']} | "
            f"{result['rows']} rows | "
            f"{result['columns']} columns"
        )

    with open("hubstaff_export_summary.md", "w", encoding="utf-8") as file:
        file.write("# Hubstaff API Export Summary\n\n")
        file.write("| File | Status | Rows | Columns | Sample Columns |\n")
        file.write("|---|---:|---:|---:|---|\n")

        for result in results:
            file.write(
                f"| {result['file']} | "
                f"{result['status']} | "
                f"{result['rows']} | "
                f"{result['columns']} | "
                f"{result['sample_columns']} |\n"
            )

    print("\nSaved: hubstaff_export_summary.md")


if __name__ == "__main__":
    main()
