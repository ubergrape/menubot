import json
import re
import os
import argparse
from datetime import datetime

import requests
from facepy import GraphAPI

from . import MenuCrawler


class FacebookCrawler:
    facebook_page_id = ""

    def get_post_from_today(self):
        # configuration

        APP_ID = os.environ.get('MENUBOT_FACEBOOK_APP_ID')
        APP_SECRET = os.environ.get('MENUBOT_FACEBOOK_APP_SECRET')

        if not APP_ID or not APP_SECRET:
            print("set MENUBOT_FACEBOOK_APP_ID and MENUBOT_FACEBOOK_APP_SECRET in your environment")
            return

        # graph api

        token = '{}|{}'.format(APP_ID, APP_SECRET)
        graph = GraphAPI(token)

        # fetch posts from facebook

        datas = graph.get(self.facebook_page_id + '/posts?fields=message,created_time', page=True, retry=1)


        # parse facebook messages

        data = ""
        message = ""
        for data in datas:
            break  # datas is a generater, we can't just do data[0]

        posts = data['data']

        today = datetime.now().date()

        for post in posts:
            created_date = datetime.strptime(post['created_time'], "%Y-%m-%dT%H:%M:%S+0000").date()
            if created_date == today:
                message = post.get('message')
                break

        return message