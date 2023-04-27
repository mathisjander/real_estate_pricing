import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# Define your target URL
base_url = "https://www.immowelt.de/liste/berlin/wohnungen/kaufen?d=true&efs=NEW_BUILDING_PROJECT&efs=JUDICIAL_SALE&sd=DESC&sf=RELEVANCE&sp="


# Function to extract listings from a single page
def extract_listings(soup):
    listings = []

    # Find listing containers (replace with the appropriate HTML structure)
    listing_containers = soup.find_all("div", class_="EstateItem-1c115")

    for listing in listing_containers:
        # Extract the listing URL
        listing_url = listing.find("a", class_="mainSection-b22fb noProject-eaed4")["href"]

        # Scrape the listing details
        listing_details = scrape_listing_details(listing_url)

        listings.append(listing_details)

    return listings


# Function to scrape details from the listing page
def scrape_listing_details(url):
    # Send request to the listing page
    listing_response = requests.get(url)
    listing_soup = BeautifulSoup(listing_response.content, "html.parser")

    # Extract information from the listing page
    try:
        energy_text = listing_soup.find("app-energy-equipment", class_="ng-star-inserted").text.strip()
        energy = re.split(r'(?=[A-ZÖ])', energy_text)[4]
        heating = re.split(r'(?=[A-ZÖ])', energy_text)[6]
    except:
        energy = 'na'
        heating = 'na'

    try:
        price = listing_soup.find("strong", class_="ng-star-inserted").text.strip().split('x')[0]
    except:
        price = 'na'

    try:
        area = listing_soup.find("span", class_="has-font-300").text.strip()
    except:
        area = 'na'

    try:
        rooms = listing_soup.find_all("span", class_="has-font-300")[1].text.strip()
    except:
        rooms = 'na'

    try:
        fee = listing_soup.find("p", class_="card-content pb-100 pb-75:400 ng-star-inserted").text.strip()[:4].replace(
            ',', '.')
    except:
        fee = 'na'

    try:
        zipcode = listing_soup.find("span", class_="has-font-100 is-bold flex flex-wrap").text.strip()[:5]
    except:
        zipcode = 'na'

    try:
        construction = listing_soup.find_all("div", class_="textlist textlist--icon card-content ng-star-inserted")[
            1].text.strip().split(' ')[1]
    except:
        construction = 'na'

    try:
        level = listing_soup.find("div", class_="equipment card-content ng-star-inserted").text.strip()[12:].split('.')[
            0]
    except:
        level = 'na'

    return {"url": url, "energy": energy, "heating": heating, "price": price
        , "area": area, 'rooms': rooms, 'fee': fee, 'zipcode': zipcode,
            "construction_year": construction, 'level': level}


# Main function to start the scraping process
def main():
    page_number = 1
    all_listings = []

    while True:
        print(f"Scraping page {page_number}")

        try:

            # Send request to the target URL
            response = requests.get(base_url + str(page_number))

            # Check if the page exists
            if response.status_code != 200:
                print("No more pages to scrape.")
                break

            soup = BeautifulSoup(response.content, "html.parser")
            listings = extract_listings(soup)

            # Check if there are listings on the page
            if not listings:
                print("No more listings to scrape.")
                break

            all_listings.extend(listings)
            page_number += 1

        except:
            pass

    print(f"Scraped {len(all_listings)} listings in total.")

    listings_df = pd.DataFrame(all_listings)
    print(listings_df)

    # Save the DataFrame to a CSV file (optional)
    listings_df.to_csv("real_estate_listings.csv", index=False)


if __name__ == "__main__":
    main()