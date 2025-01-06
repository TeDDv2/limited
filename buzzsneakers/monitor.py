import json
import time
from buzzsneakers.get_product import get_product
import database.main as database
import buzzsneakers.utils as utils
from buzzsneakers.types import Thread, ProductManager

def monitor(pid: str, parentThread: Thread):

    print('[{}] Starting thread.'.format(pid))

    while not parentThread.stop:
        data = get_product(pid)
        if not data["flag"]:
            print(f"[{pid}] Product not found.")

            if database.get_product(pid):
                database.delete_product(pid)

                # delete all sizes
                for size in data["sizes"]:
                    database.delete_size(size["combId"])

                print(f"[{pid}] Product removed from database.")
                return
            return

        if not database.get_product(pid):
            print(f"[{pid}] Product added to database.")

            product = ProductManager.build(data)
            database.add_product_to_db(product)
            utils.SendWebhook(data, "https://discord.com/api/webhooks/1223385364488523808/OZYD2h-TBcDk7X_l-t70RC21fjCOfOh7W3LcTgN0C1Jq3IqGEG9vflrc1HpiLR4seUuY", True)

        else:

            isInstock = utils.GetStockBool(data)

            if not isInstock:
                return

            product = json.loads(ProductManager.build(data))

            current_price = product["price"]
            old_price = database.get_product(pid)[3]

            if old_price != current_price:
                
                print('[{}] Price has changed. ({} -> {})'.format(pid, old_price, current_price))

                try:
                    utils.SendWebhook(data, "https://discord.com/api/webhooks/1223385364488523808/OZYD2h-TBcDk7X_l-t70RC21fjCOfOh7W3LcTgN0C1Jq3IqGEG9vflrc1HpiLR4seUuY", False)
                    database.update_product_price(pid, current_price)
                except Exception as e:
                    print(f"[{pid}] Failed to update price: {e}")

            old_quantity = database.get_product(pid)[5]
            current_quantity = product["quantity"]

            if old_quantity != current_quantity:

                print('[{}] Quantity has changed. ({} -> {})'.format(pid, old_quantity, current_quantity))

                current_sizes = product["sizes"]


                for current_size in current_sizes:
                    size = database.get_size(current_size["combId"])

                    if not size:
                        database.add_size(current_size["combId"], pid, current_size["stock"], current_size["name"], True)
                        print(f"[{pid}] Size added to database.")

                    else:
                        old_stock = float(size[2])
                        current_stock = float(current_size["stock"])

                        if old_stock != current_stock:
                            if (old_stock > 0 and current_stock == 0) or (old_stock == 0 and current_stock > 0):
                                print('[{} - {}] Quantity has changed for variant. ({} -> {})'.format(pid, current_size["combId"], old_stock, current_stock))

                                if bool(utils.GetStockBoolSizeStock(current_size)):
                                    utils.SendWebhook(data, "https://discord.com/api/webhooks/1223385364488523808/OZYD2h-TBcDk7X_l-t70RC21fjCOfOh7W3LcTgN0C1Jq3IqGEG9vflrc1HpiLR4seUuY", False)
                                database.find_size_and_update_stock(pid, current_size["combId"], current_stock)


                database.update_product_quantity(pid, current_quantity)

            


            

            """
            current_sizes = product["sizes"]

            find sizes by pid and combId and match 

            for current_size in current_sizes:
                size = database.get_size(current_size["combId"])

                if not size:
                    database.add_size_to_db(current_size)
                    print(f"[{pid}] Size added to database.")

                else:
                    old_stock = float(size[3])
                    current_stock = float(current_size["stock"])

                    if old_stock != current_stock:
                        if (old_stock > 0 and current_stock == 0) or (old_stock == 0 and current_stock > 0):
                            print('[{}] Quantity has changed for variant {}.'.format(pid, current_size["combId"]))

                            try:
                                if bool(utils.GetStockBoolSizeStock(current_size)):
                                    utils.SendWebhook(data, "https://discord.com/api/webhooks/1223385364488523808/OZYD2h-TBcDk7X_l-t70RC21fjCOfOh7W3LcTgN0C1Jq3IqGEG9vflrc1HpiLR4seUuY", False)
                                database.update_size(pid, current_size)
                            except Exception as e:
                                print(f"[{pid}] Failed to update quantity: {e}")

            
            """



"""
def monitor(pid: str, parentThread: Thread):

    print('[{}] Starting thread.'.format(pid))

    while not parentThread.stop:
            data = get_product(pid)
            if not data["flag"]:
                print(f"[{pid}] Product not found.")

                if database.check_in_db(pid, "test_buzzsneakers"):
                    database.delete_from_db(pid, "test_buzzsneakers")
                    print(f"[{pid}] Product removed from database.")
                    return
                return 
            
            if not database.check_in_db(pid, "test_buzzsneakers"):
                print(f"[{pid}] Product added to database.")

                product = ProductManager.build(data)
                database.add_to_db(pid, product,"test_buzzsneakers")
                utils.SendWebhook(data=data, webhook="https://discord.com/api/webhooks/1223385364488523808/OZYD2h-TBcDk7X_l-t70RC21fjCOfOh7W3LcTgN0C1Jq3IqGEG9vflrc1HpiLR4seUuY", backend=False)

            else:
                isInstock = utils.GetStockBool(data)

                if not isInstock:
                    return
                
                product = json.loads(ProductManager.build(data))

                current_price = product["price"]
                old_price = database.get_from_db(pid, "test_buzzsneakers")[1]["price"]

                if old_price != current_price:
                    print('[{}] Price has changed.'.format(pid))

                    try:
                        utils.SendWebhook(data=data, webhook="https://discord.com/api/webhooks/1223385364488523808/OZYD2h-TBcDk7X_l-t70RC21fjCOfOh7W3LcTgN0C1Jq3IqGEG9vflrc1HpiLR4seUuY", backend=False)
                        database.update_price(pid, current_price, "test_buzzsneakers")
                    except gspread.exceptions.APIError as e:
                        print(f"[{pid}] Failed to update price: {e}")

                old_sizes = database.get_from_db(pid, "test_buzzsneakers")[1]["sizes"]
                current_sizes = product["sizes"]
 
                if old_sizes != current_sizes:
                    for old_size in old_sizes:
                        for current_size in current_sizes:
                            if old_size["combId"] == current_size["combId"]:
                                old_stock = float(old_size["stock"])
                                current_stock = float(current_size["stock"])

                                if old_stock != current_stock:
                                    if (old_stock > 0 and current_stock == 0) or (old_stock == 0 and current_stock > 0):
                                        print('[{}] Quantity has changed for variant {}.'.format(pid, current_size["combId"]))
                                    

                                        try:
                                            if bool(utils.GetStockBoolSizeStock(current_size)):
                                                utils.SendWebhook(data=data, webhook="https://discord.com/api/webhooks/1223385364488523808/OZYD2h-TBcDk7X_l-t70RC21fjCOfOh7W3LcTgN0C1Jq3IqGEG9vflrc1HpiLR4seUuY", backend=False)
                                            database.update_size(pid, current_sizes, "test_buzzsneakers")
                                        except gspread.exceptions.APIError as e:
                                            print(f"[{pid}] Failed to update quantity: {e}")
                

"""