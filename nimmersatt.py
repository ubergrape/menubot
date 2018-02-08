from facepy import GraphAPI
import requests
import json
import re
from datetime import datetime


# configuration

webhook_url = os.environ.get('MENUBOT_WEBHOOOK_URL')

if not webhook_url:
    print("set MENUBOT_WEBHOOOK_URL in your environment")
    exit(1)

token = os.environ.get('MENUBOT_FACEBOOK_TOKEN')
# get temporary token: https://developers.facebook.com/tools/explorer/145634995501895/

if not token:
    print("set MENUBOT_FACEBOOK_TOKEN in your environment")
    exit(1)


# fetch posts from facebook

page_id = "nimmersatt.smoothies"

graph = GraphAPI(token)

datas = graph.get(page_id + '/posts?fields=message', page=True, retry=5)


# parse facebook messages

data = ""
message = ""
for data in datas:
    break  # datas is a generater, we can't just do data[0]


posts = data['data']

today = datetime.now().date()

for post in posts:
    message = post.get('message')
    created_date = datetime.strptime(post['created_time'], "%Y-%m-%dT%H:%M:%S+0000").date()
    if created_date == today and "heute" in message.lower():
        break

if message:
    food = re.findall(r'^\s*\*\s*(.+)$', message, re.M)


# send menu to Grapw

if food:
    webhook_text = "**Nimmersatt**\n\nToday, %s:\n%s" % (created_date.strftime('%A'), ''.join(['\n* ' + item for item in food]))
    payload = { 'text': webhook_text}
    requests.post(webhook_url, data=data)

else:
    print("No menu found today, try again later")
