# Hubstaff API Exporter

This project connects to the Hubstaff API using a Personal Access Token, exchanges the refresh token for an access token, and exports organization data into CSV files for reporting and analysis.

## Features

- Authenticates with Hubstaff using OAuth 2.0 refresh-token flow
- Stores rotated refresh tokens securely in a local cache file
- Exports Hubstaff organization data
- Exports Hubstaff project data
- Exports Hubstaff member data
- Exports Hubstaff activity data when available
- Generates a markdown export summary

## Exported Files

- `hubstaff_organizations.csv`
- `hubstaff_projects.csv`
- `hubstaff_members.csv`
- `hubstaff_activities.csv`
- `hubstaff_export_summary.md`

## Setup

Create a `.env` file with your Hubstaff refresh token:

```env
HUBSTAFF_REFRESH_TOKEN=your_refresh_token_here
