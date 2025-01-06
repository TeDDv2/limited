import requests
import buzzsneakers.utils as utils
from utils import exchange_rate

def GetStockBool(productData: dict) -> bool:
    return bool(float(productData['product']['quantity']) != 0)


def GetStockBoolSize(sizeData: dict) -> int:

    return (int(float(sizeData["quantity"])) != 0)


def GetStockBoolSizeStock(sizeData: dict) -> int:

    return (int(float(sizeData["stock"])) != 0)


def GetPIDFromLink(link: str) -> str:
    return link.split('/')[-1].split('-')[0]


def SendWebhook(data, webhook: str, backend:bool):
    product = data["product"]
    sizes = data["sizes"]

    url = webhook
    data = {}
    data["embeds"] = [
        {
            "title": product["name"],
            "url": f"https://www.buzzsneakers.cz/obuv/{product['id']}-limited",
            "fields": [
                {
                    "name": "SKU",
                    "value": product["productCode"],
                },
                {
                    "name": "Price",
                    "value": f"{sizes[0]['price']} CZK / {exchange_rate(round(float(sizes[0]['price'])), 'CZK', 'EUR')}€",
                },
                {
                    "name": "Region",
                    "value": f"{product['lang'].upper()}",
                },
                {
                    "name": "Sizes",
                    "value": "\n".join([f"{size['sizeName']} [{int(float(size['quantity']))}]" for size in sizes if bool(utils.GetStockBoolSize(size))]),
                },
                {
                    "name": "Links",
                    "value": f'[StockX](https://stockx.com/search?s={product["productCode"]}) | [WeTheNew](https://sell.wethenew.com/listing?keywordSearch={product["productCode"]}) | [Klekt](https://www.klekt.com/search/{product["productCode"]}) | [Goat](https://www.goat.com/search?query={product["productCode"]}) | [Laced](https://www.laced.com/search?search%5Bterm%5D={product["productCode"]})'
                }
            ],
            "thumbnail": {
                "url": f"https://www.buzzsneakers.cz/{product['image']}"
            },
            "footer": {
                "text": "buzzsneakers.cz by Limited"
            }
        }
    ]

    if backend == True:
        data["embeds"][0]["author"] = {
            "name": "Loaded on backend",
        }

    result = requests.post(url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("[{}] Webhook delivery failed, code {}.".format(product["id"], result.status_code))
    else:
        print("[{}] Webhook delivered successfully, code {}.".format(product["id"],result.status_code))
    return
