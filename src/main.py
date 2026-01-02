from constants import CLIENT_ID, CLIENT_SECRET, LOCAL_SMITHS_ID, LOCATIONS_URL, PRODUCTS_URL
from filter import eliminate_non_dairy, get_product_id
from flavor import Flavor
from krogerclient import KrogerClient
import json

def findPriceOfItem(zip_code, kroger: KrogerClient, flavor: Flavor) -> float:
    search_data = kroger.request("GET", PRODUCTS_URL, params={"filter.term": flavor.name, "filter.limit": 5})
    search_data = eliminate_non_dairy(search_data)
    product_id = get_product_id(search_data)
    
    product_data = kroger.request("GET", f"{PRODUCTS_URL}/{product_id}", params={"filter.locationId": LOCAL_SMITHS_ID})
    
    first_item = product_data.get("data")["items"][0]
    print(first_item)
    first_item_price = first_item["price"]["regular"]
    
    if first_item_price is None:
        raise ValueError(f"No price returned for itemId={first_item.get('itemId')} "
            f"(availability={first_item.get('fulfillment')})")
    
    return float(first_item_price)

def main():
    kroger = KrogerClient(CLIENT_ID, CLIENT_SECRET)
    print(str(findPriceOfItem(input("What is your zip code? "), kroger, Flavor.CHERRY_GARCIA)))

if __name__ == "__main__":
    main()