import os
import re
import locale
import calendar
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup


# configuration

webhook_url = os.environ.get('MENUBOT_WEBHOOOK_URL')

if not webhook_url:
    print("set MENUBOT_WEBHOOOK_URL in your environment")
    exit(1)

# this is needed for german day/month names from the calendar package
locale.setlocale(locale.LC_ALL, 'de_DE')


# fetch website and parse

url = "http://www.delibluem.com/bluems_mittagsmenue"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

header_text = soup.find_all('div', class_='title-1')[0].text
week = soup.find_all('div', class_='title-1')[1:6]


# check if we are on the correct weekly menu, just to be sure

m = re.search('vom (\d{1,2}) (\D+) bis (\d{1,2}) (\D+) (\d{4})', header_text)

months = [month.lower() for month in calendar.month_name]

end_month = int(months.index(m.group(4)))
end_date = date(int(m.group(5)), end_month, int(m.group(3)))
start_date = end_date - timedelta(days = 6)

if not start_date <= date.today() <= end_date:
    print("The menu is not up to date:")
    print(header_text)
    exit(1)


# find today's menu

today_name = list(calendar.day_name)[date.today().weekday()]
day_text = today_name

for day in week:
    if day.text.lower().startswith(today_name.lower()):
        day_text = day.text
        menu_text = day.fetchNextSiblings()[0].text
        break


# send menu to grape

if menu_text:
    print("Menu text found:")
    print(menu_text)
    print("Sending to Grape")
    webhook_text = "**Delibluem**\n\n{}\n{}".format(day_text, menu_text)
    payload = { 'text': webhook_text}
    requests.post(webhook_url, json=payload)
else:
    print("No menu found for {}".format(day_name))
