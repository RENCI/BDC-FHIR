# FHIR Staging to Production Migration Script

A Python script for migrating FHIR data from a staging environment to production. The script authenticates with both environments using and transfers resources via their respective FHIR REST APIs.

---

## Prerequisites

- Python 3.8+
- `pip` for installing dependencies
- Valid client credentials for both staging and production environments
---

## Configuration

The script is configured via environment variables at the top of the python file. 

### Required Environment Variables

| Variable | Description |
|---|---|
| `SINCE_DATE` | The date you want data updated from (2026-01-01 will pull in data that has been updated since January 1st 2026) |
| `STAGING_AUTH_URL` | Token endpoint for the staging environment |
| `STAGING_BASE_FHIR_URL` | Base URL for the staging FHIR server  |
| `PROD_AUTH_URL` | Token endpoint for the production environment |
| `PROD_BASE_FHIR_URL` | Base URL for the production FHIR server  |
| `STAGING_CLIENT_ID` | Client ID for authenticating with the staging environment |
| `STAGING_CLIENT_SECRET` | Client secret for authenticating with the staging environment |
| `PROD_CLIENT_ID` | Client ID for authenticating with the production environment |
| `PROD_CLIENT_SECRET` | Client secret for authenticating with the production environment |

## Usage

```bash
python loadData.py
```

The script will:
1. Authenticate with the staging FHIR server using the staging credentials
2. Authenticate with the production FHIR server using the production credentials
3. Read resources from staging
4. Write resources to production


---

# FHIR Staging Data Validation Script

A Powershell script for verifying FHIR data in the staging environment prior to pushing to production.

---
## Configuration

The script is configured via environment variables at the top of the powershell file. To create the CSV file needed - paste the Ids and Names that you are interested in into columns with the names Accession and a second column with the Name for each study. 

### Required Environment Variables

| Variable | Description |
|---|---|
| `csvFile` | A csv file with the list of ids that you want to check |
| `url` | Base URL for the staging FHIR server  |

## Usage

```bash
 .\testFHIRPhysNumbers.ps1
```

The script will:
1. Query staging for each of the ids and return whether or not they are found or missing. 

---

