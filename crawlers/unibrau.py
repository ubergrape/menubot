import re
import os
import locale
import calendar
import argparse
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

        text = text.replace('\n', ' ')  # remove line breaks
        text = ' '.join(text.split())  # remove multiple blanks

        # find menu in text

        # this is needed for german day/month names from the calendar package
        locale.setlocale(locale.LC_ALL, 'de_DE')

        today = date.today()
        today_name = list(calendar.day_name)[today.weekday()].upper()
        m = re.search(today_name + r'[, ]+?Suppe: (?P<suppe>.+?) Tagesteller: (?P<tagesteller>.+?)\s+Vegetarisch:\s+(?P<vegetarisch>.+?)\s+(?:MONTAG|DIENSTAG|MITTWOCH|DONNERSTAG|FREITAG|ÄNDERUNGEN)', text)

        if m:
            self.menu_text = "Suppe: {}\nTagesteller: {}\nVegatarisch: {}".format(m.group('suppe'), m.group('tagesteller'), m.group('vegetarisch'))
