import requests

from bs4 import BeautifulSoup


from . import MenuCrawler


class MittagAtCrawler(MenuCrawler):
    mittagat_url = ""

    def run(self):
        response = requests.get(self.mittagat_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.select('dt.today')[0].findNext('dd')
        self.menu_text = content.get_text('\n').replace('\n ', ' ')
