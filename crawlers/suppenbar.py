import re

from . import MenuCrawler
from .facebook import FacebookCrawler


class SuppenbarCrawler(MenuCrawler, FacebookCrawler):
    name = "Suppenbar"
    facebook_page_id = "Suppenbar.at"

    def run(self):
        message = self.get_post_from_today()

        if message:
            m = re.search(r'([Hh]eute .+)(\n.+)$', message, re.M)
            if m.group(2).startswith('Wir'):
                today_menu = m.group(1)
            else:
                today_menu = m.group(1) + m.group(2)

            self.menu_text = today_menu

        else:
            self.error_text = "No menu found today, try again later"
            return




        # also parse https://www.suppenbar.at/wochenkarte2

