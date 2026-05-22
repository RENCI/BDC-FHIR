import time
import requests
import sys
from datetime import datetime, timezone

# --- CONFIG ---

PAGE_SIZE = 25
SINCE_DATE = datetime(2026, 5, 1, 0, 0, 0, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

STAGING_AUTH_URL =
STAGING_BASE_FHIR_URL = 
PROD_AUTH_URL = 
PROD_BASE_FHIR_URL = 

STAGING_CLIENT_ID =
STAGING_CLIENT_SECRET =
PROD_CLIENT_ID =
PROD_CLIENT_SECRET = 


# Base URLs (Note: We use standard search path, not $export)
STAGING_SEARCH_URL = f"{STAGING_BASE_FHIR_URL}ResearchStudy?_lastUpdated=gt{SINCE_DATE}&_count={PAGE_SIZE}"
IMPORT_URL = f"{PROD_BASE_FHIR_URL}"

def get_token(auth_url, client_id, client_secret):
    """Generic token fetcher."""
    data = {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret}
    resp = requests.post(auth_url, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]

def process_page_and_get_next(url, source_token, target_token):
    """Fetches one page, imports it, and returns the next page URL."""
    headers_src = {"Authorization": f"Bearer {source_token}", "Accept": "application/fhir+json"}
    
    print(f"Fetching page: {url}")
    resp = requests.get(url, headers=headers_src)
    resp.raise_for_status()
    bundle = resp.json()

    # 1. Extract resources from the current bundle
    resources = [entry.get("resource") for entry in bundle.get("entry", []) if "resource" in entry]
    
    if resources:
        print(f"  -> Found {len(resources)} resources. Importing...")
        import_resources_to_target(resources, target_token)

    # 2. Look for the 'next' link to continue paging
    links = bundle.get("link", [])
    next_url = next((link["url"] for link in links if link["relation"] == "next"), None)
    
    return next_url

def import_resources_to_target(resources, token):
    """Converts resources into a transaction bundle and POSTs to target."""
    headers_target = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/fhir+json"
    }
    
    # We wrap the search results into a Transaction Bundle for efficiency
    transaction_bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": []
    }

    for res in resources:
        transaction_bundle["entry"].append({
            "request": {"method": "PUT", "url": f"{res['resourceType']}/{res['id']}"},
            "resource": res
        })

    resp = requests.post(IMPORT_URL, headers=headers_target, json=transaction_bundle)
    if resp.status_code >= 300:
        print(f"Import error: {resp.status_code} {resp.text[:200]}")
    else:
        print(f"Successfully imported {len(resources)} resources.")

def main():
    try:
        s_token = get_token(STAGING_AUTH_URL, STAGING_CLIENT_ID, STAGING_CLIENT_SECRET)
        p_token = get_token(PROD_AUTH_URL, PROD_CLIENT_ID, PROD_CLIENT_SECRET)

        current_url = STAGING_SEARCH_URL
        
        while current_url:
            # This loop fetches a page, uploads it, and gets the link for the next one
            current_url = process_page_and_get_next(current_url, s_token, p_token)
            
        print("\nMigration Complete. No more pages found.")

    except Exception as e:
        print(f"Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
