from flavor import Flavor
from scraper import Scraper


def main():
    scraper = Scraper()
    testresponse = scraper.getFlavorData(flavor=Flavor.CHERRY_GARCIA)
    print(testresponse.content)

if __name__ == "__main__":
    main()