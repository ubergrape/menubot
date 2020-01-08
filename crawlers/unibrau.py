import re
import locale
import calendar
from io import BytesIO
from datetime import datetime, date, timedelta

import PyPDF2
import requests
from bs4 import BeautifulSoup

from . import MenuCrawler


class UnibrauCrawler(MenuCrawler):
    name = "Unibräu"

    def run(self):

        # find current pdf on homepage

        response = requests.get('http://www.unibrau.at/')
        soup = BeautifulSoup(response.text, 'html.parser')
        pdf_url = soup.select('div.logo_holder a')[0].attrs['href']

        # download latest pdf

        response = requests.get(pdf_url)
        pdf_file = BytesIO(response.content)

        # extract text from pdf

        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        page = read_pdf.getPage(0)
        text = page.extractText()

        # bring it into a reasonable format

        text = text.replace('\n', '')  # remove line breaks
        text = ' '.join(text.split())  # remove multiple blanks

        #  is this menu for this week?

        locale.setlocale(locale.LC_ALL, 'de_AT')  # to match month names like "Jänner"
        m = re.search(r'\w+, (\d+\.\s\w+)', text)
        menu_date = datetime.strptime(m.group(1), "%d. %B").date()
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        menu_date = menu_date.replace(year=monday.year)

        if not menu_date >= monday:
            self.error_text = "Menu is for the week starting at {}, but this week's monday is {}. [menu PDF]({})".format(menu_date, monday, pdf_url)
            return

        # find menu in text

        # this is needed for german day/month names from the calendar package
        locale.setlocale(locale.LC_ALL, 'de_DE')

        today = date.today()
        today_name = list(calendar.day_name)[today.weekday()].upper()
        m = re.search(r'(' + today_name + r'.+?)(?:MONTAG|DIENSTAG|MITTWOCH|DONNERSTAG|FREITAG|ÄNDERUNGEN)', text)

        if m:
            # add some line breaks if we find a menu. if not, we will just use the text
            # sometimes they have special Feiertags text
            self.menu_text = m.group(1) \
                .replace('Suppe', '\n\nSuppe') \
                .replace('Menü 1', '\nMenü 1') \
                .replace('Vegetarisch', '\nVegetarisch')
        else:
            self.error_text = "Couldn't find today's menu in the [menu PDF]({})".format(pdf_url)
