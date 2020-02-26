import requests
from bs4 import BeautifulSoup

from . import MenuCrawler


class CafeGagarinCrawler(MenuCrawler):
    name = "Cafe Gagarin"

    def run(self):
        url = "https://cafegagarin.at/warme-speisen-und-snacks-zwischendurch"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        el = soup.find(id='block-views-tagesteller-block')
        self.menu_text = el.find(class_='content').text.strip().replace('\n\n', '\n')
