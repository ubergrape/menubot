import os
import re
import locale
import calendar
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

from . import MenuCrawler

class DelibluemCrawler(MenuCrawler):
    name = "deli bluem"


    def run(self):
        # deli bluem in the 8th district is not open on monday
        # even though there is something on the menu on the website
        if date.today().weekday() == 0:
            self.menu_text = "Closed on mondays"
            return

        # this is needed for german day/month names from the calendar package
        locale.setlocale(locale.LC_ALL, 'de_DE')


        # fetch website and parse

        url = "http://www.delibluem.com/bluems_mittagsmenue"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        header_text = soup.find_all('div', class_='title-1')[0].text
        week = soup.find_all('div', class_='title-1')[1:6]


        # check if we are on the correct weekly menu, just to be sure

        m = re.search('vom (\d{1,2}) ((\w+) )?bis (\d{1,2}) (\w+) (\d{4})', header_text)

        months = [month.lower() for month in calendar.month_name]

        end_month = int(months.index(m.group(5)))
        end_day = int(m.group(4))
        end_year = int(m.group(6))
        end_date = date(end_year, end_month, end_day)
        start_date = end_date - timedelta(days = 6)

        if not start_date <= date.today() <= end_date:
            self.error_text = "The menu is not up to date: {}".format(header_text)
            return


        # find today's menu

        today_name = list(calendar.day_name)[date.today().weekday()]
        day_text = today_name

        for day in week:
            if today_name.lower() in day.text.lower():
                text_soup = day.fetchNextSiblings()[0]
                # replace <br/> with linebreaks, otherwise everything is in one line
                for br in text_soup.find_all("br"):
                    br.replace_with("\n")
                self.menu_text = text_soup.text
                return

        self.error_text = "{} not found in menu".format(today_name)

