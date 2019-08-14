from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup

from . import MenuCrawler


class FrommeHeleneCrawler(MenuCrawler):
    name = "Fromme Helene"

    def run(self):
        # get menu html

        url = "https://www.frommehelene.at/index.php?id=15"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # is this menu for this week?

        header = soup.find('h1', class_="csc-firstHeader")
        menu_date_str = header.text.split(' ')[1]
        menu_date = datetime.strptime(menu_date_str, "%d.%m.").date().replace(year=date.today().year)
        today = date.today()
        monday = today - timedelta(days=today.weekday())

        if not menu_date == monday:
            self.error_text = "Menu is for the week starting at {}, but this week's monday is {}. [menu page]({})".format(menu_date, monday, url)
            return

        # find menu, it's in a confusing table

        table = soup.find("table", class_="contenttable")
        tds = table.findAll("td")

        start = None
        end = None
        for i, td in enumerate(tds):
            if start is None and td.text.strip().startswith("Mittwoch"):
                start = i
            if end is None and start is not None and "td-0" in td.attrs['class'] and td.text.strip() == "":
                end = i

        # get a list of menus
        menus = []
        i = 0
        for td in tds[start+1:end]:
            if i not in menus:
                menus.append("")
            menus[i] += td.text.strip() + " "
            if "td-1" in td.attrs['class'] and td.text.strip() != "":
                i += 1

        # remove empty menu lines and blanks at beginning
        menus = [item.strip() for item in menus if item != ""]

        # put the menu in self.menu_text
        self.menu_text = tds[start].text + "\n" + "\n".join(menus)
