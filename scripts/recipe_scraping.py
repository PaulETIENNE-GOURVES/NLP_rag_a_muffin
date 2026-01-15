import json
from bs4 import BeautifulSoup
from recipe_scrapers import scrape_me
import requests
import time
import random
import os
import json

url_prefix = "https://www.marmiton.org"

def get_recipe(url_prefix, url_suffix):
    url = url_prefix + url_suffix
    scraper = scrape_me(url)
    recipe_dict = scraper.to_json()
    return recipe_dict

if __name__ == "__main__":

    url_suffixes = []
    page_number = 1
    
    # Getting all the recipe URL suffixes
    print("Scraping recipe URLs...")
    while True:

        time.sleep(random.uniform(0.2, 1))

        url = f"https://www.marmiton.org/recettes/recherche.aspx?aqt=muffin"
        if page_number != 1:
            url += f"&page={page_number}"
        
        r = requests.get(url, allow_redirects=True)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, features="html.parser")
        elements = soup.findAll(class_='card-content__title')
        for elt in elements:
            suffix = elt.get('href')
            url_suffixes.append(suffix)
        print(f"Scraped page {page_number}")
        page_number += 1

    print(f"Found {len(url_suffixes)} recipes.")
    
    # Scraping each recipe
    for k, url_suffix in enumerate(url_suffixes):

        time.sleep(random.uniform(0.5, 1.5))

        recipe = get_recipe(url_prefix, url_suffix)

        if "title" in recipe.keys():
            print("Scraping ", recipe["title"], " ...")
        
        # Saving each recipe as a JSON file
        os.makedirs("./data", exist_ok=True)
        with open(f"./data/recipe{k}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(recipe, ensure_ascii=False, indent=4))




