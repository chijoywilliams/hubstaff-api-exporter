"""
Hubstaff API Exporter — Demo Mode

Generates synthetic organization, project, member, and activity data in the same
schema the real exporter produces from the Hubstaff API. Useful for demonstrating
the pipeline, running the code path, and verifying CSV/Markdown output when a live
Hubstaff account is not available.

The OAuth 2.0 refresh-token flow and live API calls used in production live in the
sibling scripts (export_hubstaff_orgs.py, export_hubstaff_projects.py, etc.).
This script exercises the same output stage — CSV writing and Markdown summary —
without hitting the network.

Usage:
    python export_hubstaff_demo.py
"""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
RUN_TIMESTAMP = datetime.now(timezone.utc)


def _write_csv(filename: str, rows: list[dict]) -> Path:
    path = OUTPUT_DIR / filename
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def build_organizations() -> list[dict]:
    return [
        {
            "id": 1001,
            "name": "Demo Consulting LLC",
            "status": "active",
            "created_at": "2024-03-14T10:22:00Z",
            "last_activity": RUN_TIMESTAMP.isoformat(),
        },
        {
            "id": 1002,
            "name": "Sample Studio Co",
            "status": "active",
            "created_at": "2024-08-01T09:00:00Z",
            "last_activity": RUN_TIMESTAMP.isoformat(),
        },
    ]


def build_projects() -> list[dict]:
    names = [
        "Website Redesign",
        "Mobile App v2",
        "Client Onboarding Automation",
        "Data Warehouse Migration",
        "Internal Ops Dashboard",
        "Marketing Site Refresh",
    ]
    return [
        {
            "id": 2000 + i,
            "organization_id": 1001 if i % 2 == 0 else 1002,
            "name": name,
            "status": "active" if i < 5 else "archived",
            "billable": "true" if i % 2 == 0 else "false",
            "created_at": (RUN_TIMESTAMP - timedelta(days=30 + i * 5)).isoformat(),
        }
        for i, name in enumerate(names)
    ]


def build_members() -> list[dict]:
    people = [
        ("Alex Rivera", "alex.rivera@example.com", "developer"),
        ("Priya Shah", "priya.shah@example.com", "designer"),
        ("Marcus Lee", "marcus.lee@example.com", "project_manager"),
        ("Jordan Kim", "jordan.kim@example.com", "developer"),
        ("Sam Okafor", "sam.okafor@example.com", "qa"),
    ]
    return [
        {
            "id": 3000 + i,
            "organization_id": 1001,
            "name": name,
            "email": email,
            "role": role,
            "status": "active",
        }
        for i, (name, email, role) in enumerate(people)
    ]


def build_activities(members: list[dict], projects: list[dict]) -> list[dict]:
    random.seed(42)
    rows: list[dict] = []
    activity_id = 4000
    for day_offset in range(5):
        day = RUN_TIMESTAMP - timedelta(days=day_offset)
        for member in members:
            for project in random.sample(projects, k=2):
                tracked_seconds = random.randint(1800, 14400)  # 30 min – 4 hrs
                rows.append(
                    {
                        "id": activity_id,
                        "date": day.date().isoformat(),
                        "user_id": member["id"],
                        "user_name": member["name"],
                        "project_id": project["id"],
                        "project_name": project["name"],
                        "tracked_seconds": tracked_seconds,
                        "tracked_hours": round(tracked_seconds / 3600, 2),
                        "activity_percent": random.randint(55, 95),
                    }
                )
                activity_id += 1
    return rows


def write_summary(files: dict[str, tuple[Path, int]]) -> Path:
    lines = [
        "# Hubstaff Export Summary (Demo Mode)",
        "",
        f"Run timestamp: {RUN_TIMESTAMP.isoformat()}",
        "",
        "Source: **synthetic demo data** (no live Hubstaff API calls).",
        "The production scripts in this repo use OAuth 2.0 refresh tokens to pull",
        "the same schema from the Hubstaff REST API.",
        "",
        "## Generated files",
        "",
        "| File | Records |",
        "|---|---:|",
    ]
    for label, (path, count) in files.items():
        lines.append(f"| `{path.name}` | {count} |")
    lines.append("")
    summary_path = OUTPUT_DIR / "hubstaff_export_summary.md"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return summary_path


def main() -> None:
    print(f"[demo] Hubstaff API Exporter — demo mode")
    print(f"[demo] Run started at {RUN_TIMESTAMP.isoformat()}")
    print("[demo] No live API calls — generating synthetic data in the production schema.\n")

    organizations = build_organizations()
    projects = build_projects()
    members = build_members()
    activities = build_activities(members, projects)

    files = {
        "organizations": (_write_csv("hubstaff_organizations.csv", organizations), len(organizations)),
        "projects": (_write_csv("hubstaff_projects.csv", projects), len(projects)),
        "members": (_write_csv("hubstaff_members.csv", members), len(members)),
        "activities": (_write_csv("hubstaff_activities.csv", activities), len(activities)),
    }

    for label, (path, count) in files.items():
        print(f"[demo] wrote {path.name:<32} {count:>4} records")

    summary_path = write_summary(files)
    print(f"[demo] wrote {summary_path.name}")
    print("\n[demo] Done. Open the CSVs or the summary Markdown to inspect the output.")


if __name__ == "__main__":
    main()
