import re
import locale
from datetime import datetime, date

import requests
from bs4 import BeautifulSoup

from . import MenuCrawler


class KrauterdrogerieCrawler(MenuCrawler):
    name = "Kräuterdrogerie"

    def run(self):

        # fetch website and parse

        url = "https://www.kraeuterdrogerie.at/essen"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # the website has no date in the content, so let's hope the menu
        # really is for today.

        # extract text from website

        h3_items = soup.select('#block-yui_3_17_2_1_1588614159586_48902 h3')[:-1]
        self.menu_text = '\n'.join(item.text.strip() for item in h3_items)
