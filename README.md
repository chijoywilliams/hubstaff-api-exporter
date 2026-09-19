# Hubstaff API Exporter

A Python-based automation tool that securely connects to the Hubstaff API and exports organization, project, member, and available activity data into CSV files for reporting, analysis, and downstream business workflows.

## Overview

Hubstaff data is often needed outside the platform for operational reporting, project analysis, staffing visibility, payroll review, or integration with internal tools. Manually collecting and organizing these exports is repetitive and can introduce errors.

Hubstaff API Exporter automates this workflow. It uses Hubstaff's OAuth 2.0 refresh-token flow to obtain an access token, retrieves available organization-level data, saves the results in structured CSV files, and creates a Markdown summary of the export run.

## Features

- Authenticates with Hubstaff through the OAuth 2.0 refresh-token flow
- Uses a refresh token to request an access token
- Exports Hubstaff organization data
- Exports Hubstaff project data
- Exports Hubstaff member data
- Exports activity data when it is available to the connected account
- Generates structured CSV files for reporting and analysis
- Creates a Markdown export summary for each completed run
- Uses environment variables to keep credentials outside source control


## Exported Files

| File | Description |
|---|---|
| `hubstaff_organizations.csv` | Organization information returned by the Hubstaff API |
| `hubstaff_projects.csv` | Project data associated with the available organization(s) |
| `hubstaff_members.csv` | Organization member data returned by the API |
| `hubstaff_activities.csv` | Available activity data, when supported and accessible |
| `hubstaff_export_summary.md` | Summary of the export run, including generated files and record counts |

## Requirements

- Python [version used by this project]
- A Hubstaff account with API access
- A Hubstaff OAuth 2.0 refresh token
- Access to the Hubstaff organizations and data being exported

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/chijoywilliams/hubstaff-api-exporter.git
   cd hubstaff-api-exporter
