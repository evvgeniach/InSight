import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COMPANIES_HOUSE_API_KEY")
BASE_URL = "https://api.company-information.service.gov.uk"

def search_companies(industry, num_results=100):
    rows = []
    url = f"{BASE_URL}/search/companies"

    params = {
        "q": industry,
        "items_per_page": 20
    }

    # fetch 5 pages = 100 companies
    for page in range(5):
        params["start_index"] = page * 20
        response = requests.get(
            url,
            params=params,
            auth=(API_KEY, "")  # Companies House uses API key as username
        )
        data = response.json()
        items = data.get("items", [])

        for item in items:
            rows.append({
                "company_name": item.get("title"),
                "company_number": item.get("company_number"),
                "status": item.get("company_status"),
                "type": item.get("company_type"),
                "incorporated_date": item.get("date_of_creation"),
                "address": item.get("address_snippet"),
                "description": item.get("description")
            })

        print(f"Page {page + 1} fetched — {len(items)} companies")

    return pd.DataFrame(rows)

if __name__ == "__main__":
    print("Fetching companies...")
    df = search_companies("fintech")
    df.to_csv("demo_data/companies_house.csv", index=False)
    print(f"Done — {len(df)} companies saved to demo_data/companies_house.csv")
    print(df.head())