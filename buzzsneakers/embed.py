import discord
from utils import exchange_rate

def embed_builder(data: dict):
    product = data["product"]
    sizes = data["sizes"]
    embed = discord.Embed(title=product["name"], url=f"https://www.buzzsneakers.cz/obuv/{product['id']}-limited", color=0x546e7a)
    embed.add_field(name="SKU", value=product["productCode"], inline=True)
    embed.add_field(name="Price", value=f"{sizes[0]['price']} CZK / {exchange_rate(round(float(sizes[0]['price'])), 'CZK', 'EUR')}€", inline=True)
    embed.add_field(name="Region", value=f"{product['lang'].upper()}", inline=True)
    embed.set_thumbnail(url=f"https://www.buzzsneakers.cz/{product['image']}")
    embed.set_footer(text="Buzzsneakers Limited")
    sizes = [f"{size['sizeName']} [{int(float(size['quantity']))}]" for size in sizes if float(size['quantity']) > 0]
    if not sizes:
        sizes = ["No sizes available"]
    embed.add_field(name="Sizes", value="\n".join(sizes))
    embed.add_field(name="Links", value=f'[StockX](https://stockx.com/search?s={product["productCode"]})'
                                        f' | [WeTheNew](https://sell.wethenew.com/listing?keywordSearch={product["productCode"]})'
                                        f' | [Klekt](https://www.klekt.com/search/{product["productCode"]})'
                                        f' | [Goat](https://www.goat.com/search?query={product["productCode"]})'
                                        f' | [Laced](https://www.laced.com/search?search%5Bterm%5D={product["productCode"]})', inline=False)
    return embed