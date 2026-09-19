# Hubstaff API Exporter

A Python-based automation tool that connects to the Hubstaff API and exports available organization, project, member, and activity data into CSV files for reporting, analysis, and downstream business workflows.

## Overview

Hubstaff data is often needed outside the platform for operational reporting, project analysis, staffing visibility, payroll review, or integration with internal tools. Manually collecting and organizing exports is repetitive and can introduce errors.

Hubstaff API Exporter uses Hubstaff's OAuth 2.0 refresh-token flow to request an access token, retrieve available organization, project, member, and activity data, save the results in structured CSV files, and create a Markdown summary of the export run.

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

- Python 3.11
- A Hubstaff account with API access
- A Hubstaff OAuth 2.0 refresh token
- Authorization to access the Hubstaff organizations and data being exported

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/chijoywilliams/hubstaff-api-exporter.git
   cd hubstaff-api-exporter
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   On macOS or Linux:

   ```bash
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root using `.env.example` as a template:

   ```bash
   cp .env.example .env
   ```

   On Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

5. Add your Hubstaff refresh token to `.env`:

   ```env
   HUBSTAFF_REFRESH_TOKEN=replace_with_your_refresh_token
   ```

6. Run the exporter scripts:

   ```bash
   python export_hubstaff_orgs.py
   python export_hubstaff_projects.py
   python export_hubstaff_members.py
   python export_hubstaff_activities.py
   ```

## Security

- Do not commit `.env`, refresh tokens, access tokens, local token-cache files, or exports containing sensitive organization or employee data.
- Use only Hubstaff accounts and organizations you are authorized to access.
- Revoke and replace a credential immediately if it is exposed.
- Review exported files before sharing them, as they may contain sensitive data.

## Skills Demonstrated

- Python scripting and automation
- REST API integration
- OAuth 2.0 refresh-token authentication
- Environment-based configuration
- Data extraction and CSV reporting
- Technical documentation and repeatable setup

## Disclaimer

This project is an independent integration and is not affiliated with or endorsed by Hubstaff.
