import json
import requests
from flavor import Flavor

class Scraper:
    def __init__(self):
        with open('data/baseRequests.json', 'r') as file:
            self.baseRequests = json.load(file)
    
    def getFlavorData(self, flavor: Flavor):
        if flavor.name not in self.baseRequests:
            print(f"Flavor '{flavor.name}' not found")
            return
        
        url = self.baseRequests[flavor.name]["url"]
        payload = self.baseRequests[flavor.name]["payload"]
        headers = self.baseRequests[flavor.name]["headers"]
        
        response = requests.request("GET", url, headers=headers, data=payload)
        
        return response