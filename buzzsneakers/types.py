import json
import threading

class Size:
    def __init__(self, combId: str, stock: int, name: str):
        self.combId = combId
        self.stock = stock
        self.name = name
        self.change_price = False
        self.change_stock = False

    def __repr__(self):
        return f"Size(combId={self.combId}, stock={self.stock}, name={self.name})"


class ProductManager:
    @staticmethod
    def build(data: dict) -> str:
        product_info = data["product"]
        sizes_info = data["sizes"]

        # Building the product dictionary with necessary and dynamic fields
        product_dict = {
            'pid': product_info.get("id"),
            'sku': product_info.get("productCode"),
            'name': product_info.get("name"),
            'price': int(float(sizes_info[0].get("price"))),
            'image': product_info.get("image"),
            'quantity': int(float(product_info.get("quantity"))),
            'sizes': [
                {
                    "combId": size.get("productCombinationId"),
                    "stock": int(float(size.get("quantity"))),
                    "name": size.get("sizeName"),
                    "updated_size": False,
                }
                for size in sizes_info
            ],
            "deleted": False,
            "updated_price": False,
        }
        
        return json.dumps(product_dict, indent=2)


class Thread:
    def __init__(self, flow, pid):
        self.pid = pid
        self.flow = flow
        self.stop = False
        self.thread = threading.Thread(target=self.flow, args=(self.pid, self))

    def start(self):
        self.thread.start()

    def Stop(self):
        self.stop = True