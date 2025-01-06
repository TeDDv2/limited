import requests

def get_product(PID: str):
    
    #print("[{}] Getting product info.".format(PID))


    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Origin': 'https://www.buzzsneakers.cz',
        'Pragma': 'no-cache',
        'Referer': 'https://www.buzzsneakers.cz/tenisky/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    data = {
        "nbAjax": 1,
        "task": "getproductdata",
        "productId": PID
    }

    response = requests.post(f"https://www.buzzsneakers.cz/tenisky/", headers=headers, data=data)

    if response.status_code != 200:
        raise Exception("[{}] Failed to get product info [{}]".format(PID, response.status_code))
    
    if "Produkt nenalezen" in response.text:
        response = {
            "flag": False
        }
        return response

    return response.json()