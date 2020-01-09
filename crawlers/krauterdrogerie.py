import re
import locale
from datetime import datetime, date

import requests
from bs4 import BeautifulSoup

from . import MenuCrawler


class KrauterdrogerieCrawler(MenuCrawler):
    name = "Kräuterdrogerie"

    def run(self):
        # TODO: your code

        # fetch website and parse

        url = "https://www.kraeuterdrogerie.at/mittagsmenue"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        #  is this menu for today?

        locale.setlocale(locale.LC_ALL, 'de_AT')  # to match month names like "Jänner"
        menu_date_text = soup.find_all('h2')[0].text
        # remove the day name because they make typos like "Donnestag"
        menu_date_text = menu_date_text.split(',')[1].strip()
        menu_date = datetime.strptime(menu_date_text, "%d. %B").date()
        today = date.today()
        menu_date = menu_date.replace(year=today.year)

        if not menu_date == today:
            self.error_text = "Menu is for {}, but today is {}. [menu website]({})".format(menu_date, today, url)
            return

        # extract text from website

        self.menu_text = soup.find_all('div', class_='menu')[0].text.strip()
        self.menu_text = self.menu_text.replace("\n\n\n", "\n")
