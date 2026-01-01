from constants import CLIENT_ID, CLIENT_SECRET
from flavor import Flavor
from krogerclient import KrogerClient
import dotenv

def main():
    kroger = KrogerClient(CLIENT_ID, CLIENT_SECRET)

    products_url = "https://api.kroger.com/v1/products"
    data = kroger.request("GET", products_url, params={"filter.term": "Cherry Garcia", "filter.limit": 5})
    print(data)

if __name__ == "__main__":
    main()