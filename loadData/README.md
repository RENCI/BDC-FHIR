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

## Security Notes

- **Never commit credentials** — add `.env` to your `.gitignore`
- Treat `CLIENT_SECRET` values like passwords; rotate them if they are ever exposed
- Use short-lived tokens and ensure the auth URLs support token expiry/refresh as needed
- Restrict production credentials to the minimum required FHIR scopes

---

## Troubleshooting

**Authentication errors**
Verify that `AUTH_URL`, `CLIENT_ID`, and `CLIENT_SECRET` are correct for the target environment. Confirm the client has the required OAuth scopes.

**Connection errors**
Check that `BASE_FHIR_URL` does not have a trailing slash and is reachable from your network.

**Missing environment variables**
The script will exit with a clear error message listing any unset required variables. Double-check your `.env` file or shell exports.

---

## License

[Add your license here]

