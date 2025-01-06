import requests
import math

def exchange_rate(amount: int, fr: str, to: str):
    headers = {
        "accept-language": "en"
    }
    if type(amount) != int:
        raise Exception("Amount must be an integer")

    url = f"https://www.revolut.com/api/exchange/quote?amount={amount}&country=GB&fromCurrency={fr}&isRecipientAmount=false&toCurrency={to}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to get exchange rate")
    
    return response.json()["recipient"]["amount"]
    

def round_up_and_choose_nearest(number):
    return math.ceil(number / 500) * 500


def format_size(size):

    if '1/3' in size:
        return size.replace(' 1/3', ' 1/3')
    elif '1/2' in size:
        return size.replace(' 1/2', ',5')
    elif '2/3' in size:
        return size.replace(' 2/3', ' 2/3')
    else:
        return size.replace(".", ",")
    

def wise_exchange_rate(source: str, target: str): 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Authorization": "Basic OGNhN2FlMjUtOTNjNS00MmFlLThhYjQtMzlkZTFlOTQzZDEwOjliN2UzNmZkLWRjYjgtNDEwZS1hYzc3LTQ5NGRmYmEyZGJjZA=="
    }

    response = requests.get(f"https://api.wise.com/v1/rates?source={source}&target={target}", headers=headers)
    data = response.json()[0]["rate"]
    
    if response.status_code != 200:
        raise Exception(f"Failed to get exchange rate: {data}")

    return data