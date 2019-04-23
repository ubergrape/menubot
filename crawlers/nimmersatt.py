import json
import re
import os
import argparse
from datetime import datetime

import requests
from facepy import GraphAPI

from . import MenuCrawler
from .facebook import FacebookCrawler


# nimmersatt is dead, this is just left here as an example on how to use
# the facebook crawler

class NimmersattCrawler(MenuCrawler, FacebookCrawler):
    name = "Nimmersatt"
    facebook_page_id = "nimmersatt.smoothies"

    def run(self):
        message = self.get_post_from_today()

        if message:
            food = re.findall(r'^\s*\*\s*(.+)$', message, re.M)
        else:
            self.error_text = "No menu found today, try again later"
            return

        self.menu_text = ''.join(['\n* ' + item for item in food])
