import requests
import xmltodict
import time
import database.main as database
import buzzsneakers.utils as utils
from buzzsneakers.get_product import get_product
import json
from buzzsneakers.types import Thread, ProductManager

def backend(_, parentThread: Thread):

    while True:
        try:
            time.sleep(60)
            keywords = ["nike", "adidas", "new-balance", "asics"]
            try:
                response = requests.get("https://www.buzzsneakers.cz/files/sitemap/CZE_cz/product.xml")

            except requests.exceptions.ConnectionError or requests.exceptions.ConnectTimeout:
                print("[BACKEND] Connection error.")
                continue
        
            if response.status_code != 200:
                print("[BACKEND] Failed to fetch data.")
                continue

            try:
                data = xmltodict.parse(response.text)
            except xmltodict.expat.ExpatError:
                print("[BACKEND] Error parsing XML.")
                continue

            if not data["urlset"].get("url"):
                print("[BACKEND] No links found.")
                continue
            
            for url in data["urlset"]["url"]:
                loc = url["loc"].strip().lower()
                if "tenisky" in loc and any(keyword in loc for keyword in keywords):

                    pid = utils.GetPIDFromLink(url["loc"])
                    if not database.get_product(pid):

                        data = get_product(pid)
                        product = ProductManager().build(data)
                        database.add_product_to_db(product)
                        utils.SendWebhook(data, "https://discord.com/api/webhooks/1223385364488523808/OZYD2h-TBcDk7X_l-t70RC21fjCOfOh7W3LcTgN0C1Jq3IqGEG9vflrc1HpiLR4seUuY", True)

                        print("[BACKEND] Added to database. {}".format(pid))

                    continue
            break
        except Exception as e:
            print("[BACKEND] Error: {}".format(e))
            continue