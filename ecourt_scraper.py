import requests
from bs4 import BeautifulSoup
import json
import argparse
from utils.helpers import save_json, download_pdf

BASE_URL = "https://services.ecourts.gov.in/ecourtindia_v6/"

def get_case_details(cnr=None, case_type=None, case_no=None, year=None):
    """Fetch case listing details."""
    if cnr:
        url = f"{BASE_URL}?p=cnr_status&cnr={cnr}"
    else:
        url = f"{BASE_URL}?p=case_status&case_type={case_type}&case_no={case_no}&year={year}"

    print(f"Fetching details from: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print("Error: Unable to reach eCourts website.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def check_case_listing(soup, day):
    """Check if the case is listed today or tomorrow."""
    listings = soup.find_all('tr')
    results = []
    for row in listings:
        text = row.get_text(strip=True)
        if day in text.lower():
            results.append(text)
    return results

def main():
    parser = argparse.ArgumentParser(description="eCourts Scraper CLI")
    parser.add_argument("--cnr", help="CNR number")
    parser.add_argument("--case_type", help="Case type (e.g. CR, CIVIL)")
    parser.add_argument("--case_no", help="Case number")
    parser.add_argument("--year", help="Case year")
    parser.add_argument("--today", action="store_true", help="Check listing for today")
    parser.add_argument("--tomorrow", action="store_true", help="Check listing for tomorrow")
    parser.add_argument("--causelist", action="store_true", help="Download full cause list")

    args = parser.parse_args()
    day = "today" if args.today else "tomorrow" if args.tomorrow else "today"

    soup = get_case_details(args.cnr, args.case_type, args.case_no, args.year)
    if not soup:
        return

    results = check_case_listing(soup, day)
    if results:
        print(f"✅ Case is listed {day}:")
        for r in results:
            print(r)
        save_json(results, f"data/results_{day}.json")
    else:
        print(f"❌ Case is not listed {day}.")

    if args.causelist:
        download_pdf(BASE_URL + "cause_list.pdf", "data/cause_list.pdf")

if __name__ == "__main__":
    main()
