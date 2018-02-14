import json
import re
import os
import argparse
from datetime import datetime

import requests
from facepy import GraphAPI


parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true",
                    help="Write webhook text to stdout, don't send to Grape")
args = parser.parse_args()


# configuration

webhook_url = os.environ.get('MENUBOT_WEBHOOOK_URL')

if not webhook_url and not args.dry_run:
    print("set MENUBOT_WEBHOOOK_URL in your environment")
    exit(1)

APP_ID = os.environ.get('MENUBOT_FACEBOOK_APP_ID')
APP_SECRET = os.environ.get('MENUBOT_FACEBOOK_APP_SECRET')

if not APP_ID or not APP_SECRET:
    print("set MENUBOT_FACEBOOK_APP_ID and MENUBOT_FACEBOOK_APP_SECRET in your environment")
    exit(1)


# fetch posts from facebook

page_id = "nimmersatt.smoothies"

token = '{}|{}'.format(APP_ID, APP_SECRET)
graph = GraphAPI(token)

datas = graph.get(page_id + '/posts?fields=message,created_time', page=True, retry=1)


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

if message:
    food = re.findall(r'^\s*\*\s*(.+)$', message, re.M)


# send menu to Grape

if food:
    webhook_text = "**Nimmersatt**\n\nToday, %s:\n%s" % (created_date.strftime('%A'), ''.join(['\n* ' + item for item in food]))
    if args.dry_run:
        print(webhook_text)
    else:
        payload = { 'text': webhook_text}
        requests.post(webhook_url, data=data)

else:
    print("No menu found today, try again later")
