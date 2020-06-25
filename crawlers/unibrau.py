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
        pdf_links = soup.select('#pdfmenu_div a')
        pdf_url = next(filter(lambda x: x.text.strip() == "Tageskarte", pdf_links)).attrs['href']

        self.menu_text = "check out [the weekly menu pdf](%s)" % pdf_url
        return


        # TODO

        # download latest pdf

        response = requests.get(pdf_url)
        pdf_file = BytesIO(response.content)

        # extract text from pdf

        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        page = read_pdf.getPage(0)
        text = page.extractText()

        # bring it into a reasonable format

        text = text.replace('\n \n', '\n')  # remove double line breaks
        text = text.replace('\n\n', '\n')
        text = text.replace('\n\n', '\n')

        # is this menu for this week? no date in pdf anymore

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
