import re
from io import BytesIO

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import requests
from bs4 import BeautifulSoup

from . import MenuCrawler


class Guru1080Crawler(MenuCrawler):
    name = "Guru1080"

    def run(self):
        # get image url

        url = "https://www.guru1080.at/wochenmen%C3%BC/"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        img_dom = soup.select('#content_area img')

        if img_dom:
            img_url = img_dom[0].attrs['src']
        else:
            self.error_text = "Menu image not found, please check the [menu page]({})".format(url)
            return

        # download image

        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))

        # upscale image because tesseract doesn't work properly with small text
        # https://stackoverflow.com/questions/4909396/is-there-any-way-to-improve-tesseract-ocr-with-small-fonts

        width, height = img.size
        img_resized = img.resize((width*4, height*4), Image.LANCZOS)

        # parse text

        text = pytesseract.image_to_string(img_resized, lang='deu')

        # clean text

        # strip stupid OCR bullshit results
        p = re.compile('[A-Z ]+\n')
        text = p.sub("",text)

        # strip single character lines lol
        p = re.compile('^.\n', flags=re.MULTILINE)
        text = p.sub("",text)

        # strip bio-vegan
        p = re.compile('.*bio-vegan.*\n')
        text = p.sub("",text)

        # strip multiple new lines
        p = re.compile('\n+')
        text = p.sub("\n",text).strip()

        self.menu_text = text
