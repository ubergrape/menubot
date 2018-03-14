import re
import os
import locale
import calendar
import argparse
from io import BytesIO
from datetime import datetime, date, timedelta

import PyPDF2
import requests

from . import MenuCrawler


class GanglCrawler(MenuCrawler):
    name = "Gangl"

    def run(self):

        # ------------------------------------------------------------------------------
        # find current pdf on homepage
        # ------------------------------------------------------------------------------

        response = requests.get('http://www.gangl.at/')

        # don't parse with BeautifulSoup, you won't find the link to the pdf.
        # The link to the pdf is inserted via JS into the DOM:
        #   <script>
        #   var link = 'http://www.gangl.at/wp-content/uploads/2018/02/Wochenmenüplan-3.pdf';
        #   jQuery( document ).ready(function() {
        #       jQuery('a[href="#mittagsmenu"]').attr("href", link);
        #   });
        #   </script>

        pdf_url = re.search(r"var link = '(\S+)';", response.text).group(1)

        # ------------------------------------------------------------------------------
        # download latest pdf
        # ------------------------------------------------------------------------------

        response = requests.get(pdf_url)
        pdf_file = BytesIO(response.content)

        # ------------------------------------------------------------------------------
        # extract text from pdf
        # ------------------------------------------------------------------------------

        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        page = read_pdf.getPage(0)
        text = page.extractText()

        # looks like shit:

        # T
        # agesteller
        #
        # ab
        # Montag
        #
        # 12
        # .
        # 02
        # .201
        # 8

        # bring it into a reasonable format
        # don't use regex because this is much easier
        text = text.replace('\n \n','xxxx')\
                   .replace('\n','')\
                   .replace('xxxx','\n')\
                   .replace('\n ', '\n')

        # is this menu for this week?

        # should be the third line in the text
        menu_date_str = text.split('\n')[2]
        menu_date = datetime.strptime(menu_date_str, "%d.%m.%Y").date()
        today = date.today()
        monday = today - timedelta(days=today.weekday())

        if not menu_date >= monday:
            self.error_text = "Menu is for the week starting at {}, but this week's monday is {}".format(menu_date, monday)
            return

        # ------------------------------------------------------------------------------
        # find menu in text
        # ------------------------------------------------------------------------------

        # this is needed for german day/month names from the calendar package
        locale.setlocale(locale.LC_ALL, 'de_DE')

        today_name = list(calendar.day_name)[today.weekday()]
        m = re.search(today_name + r'(?:\:?)\n([\s\S]*?)T1:([\s\S]*?)T2:([\s\S]*?)(?:Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Wochenangebot)', text)

        if m:
            suppe = m.group(1).replace('\n',' ')
            t1 = m.group(2).replace('\n',' ')
            t2 = m.group(3).replace('\n',' ')
            self.menu_text = "T1: {}\nT2: {}".format(suppe, t1, t2)
