import requests
import logging
from airflow.operators.python import get_current_context
import json
def call_api(page_name):
    base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/desktop/user"
    url = f"{base_url}/{page_name}/daily/20230821/20230821"
    headers = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "User-Agent": "Meow I am pusheen the cat. Meow.",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    text = response.text
    logging.info(text)
    obj = response.json()
    logging.info(json.dumps(obj))
    
call_api("Azathoth")
list_of_tracked_wiki = [
    "Cthulhu_Mythos",
    "Cthulhu_Mythos_deities",
    "Elder_God_(Cthulhu_Mythos)",
    "Ghatanothoa",
    "Nyarlathotep",
    "Azathoth",
    "Cult_(religious_practice)",
    "Cthulhu",
    "Wikiwand",
    "Company_scrip",
    "At_the_Mountains_of_Madness"
]

for wiki in list_of_tracked_wiki:
    print("======== wiki " + wiki+ "=================") 
    call_api(wiki)