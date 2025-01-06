import json
from buzzsneakers.types import ProductManager as BuzzsneakersProductManager
from sportvision.types import ProductManager as SportvisionProductManager
from buzzsneakers.get_product import get_product as buzzsneakers_get_product
from sportvision.get_product import get_product as sportvision_get_product
from typing import Dict, List

def create_best_product(buzzsneakers_id: str, sportvision_id: str) -> Dict:
    buzzsneakers_data = buzzsneakers_get_product(buzzsneakers_id)
    sportvision_data = sportvision_get_product(sportvision_id)
    
    if buzzsneakers_data["product"]["productCode"] != sportvision_data["product"]["productCode"]:
        raise ValueError("Product codes do not match")

    buzzsneakers_product = json.loads(BuzzsneakersProductManager.build(buzzsneakers_data))
    sportvision_product = json.loads(SportvisionProductManager.build(sportvision_data))
    
    # Vybrat produkt s nižší cenou
    best_product = min([buzzsneakers_product, sportvision_product], key=lambda p: p['price'])
    
    # Vytvořit slovník pro uchování nejlepších velikostí
    best_sizes: Dict[str, Dict] = {}
    
    # Projít velikosti obou produktů a vybrat ty s nejvyšším množstvím
    for product, source in [(buzzsneakers_product, 'Buzzsneakers'), (sportvision_product, 'Sportvision')]:
        for size in product['sizes']:
            if size['name'] not in best_sizes or size['stock'] > best_sizes[size['name']]['stock']:
                size_copy = size.copy()
                size_copy['source'] = source
                best_sizes[size['name']] = size_copy
    
    # Seřadit velikosti podle názvu
    sorted_sizes = sorted(best_sizes.values(), key=lambda s: float(s['name']) if s['name'].replace('.', '').isdigit() else s['name'])
    
    # Vytvořit nový produkt s nejlepšími vlastnostmi
    new_product = {
        'pid': best_product['pid'],
        'sku': best_product['sku'],
        'name': best_product['name'],
        'price': best_product['price'],
        'image': best_product['image'],
        'quantity': sum(size['stock'] for size in sorted_sizes),
        'sizes': sorted_sizes,
        'deleted': False,
        'updated_price': False,
        'source': 'Buzzsneakers' if best_product['price'] == buzzsneakers_product['price'] else 'Sportvision',
        'buzzsneakers_price': buzzsneakers_product['price'],
        'sportvision_price': sportvision_product['price']
    }
    
    return new_product

def print_product_details(product: Dict):
    print(f"Nejlepší produkt:")
    print(f"Název: {product['name']}")
    print(f"SKU: {product['sku']}")
    print(f"Nejnižší cena: {product['price']} (Zdroj: {product['source']})")
    print(f"Cena Buzzsneakers: {product['buzzsneakers_price']}")
    print(f"Cena Sportvision: {product['sportvision_price']}")
    print(f"Cenový rozdíl: {abs(product['buzzsneakers_price'] - product['sportvision_price'])}")
    print(f"Celkové množství: {product['quantity']}")
    print("Dostupné velikosti:")
    for size in product['sizes']:
        if size['stock'] > 0:
            print(f"  - {size['name']}: {size['stock']} ks (Zdroj: {size['source']})")

def best_of_best():
    best_product = create_best_product("24457", "69868")
    print_product_details(best_product)

if __name__ == "__main__":
    best_of_best()

