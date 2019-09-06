try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# TODO: prepare:
# - proper crawler code
# - pip install pytesseract
# - install tesseract https://github.com/tesseract-ocr/tesseract
# - download "deu" training data https://github.com/tesseract-ocr/tessdata/blob/master/deu.traineddata
# - mv deu.traineddata /usr/local/share/tessdata
#

# get image url

# https://www.guru1080.at/wochenmen%C3%BC/

# TODO

# download image

# TODO

# upscale image
# tesseract doesn't work properly with small text
# https://stackoverflow.com/questions/4909396/is-there-any-way-to-improve-tesseract-ocr-with-small-fonts

# TODO: use PIL or imagemagick via python
# convert -resize 600% menu.png menu600.png



# parse text

filename = 'menu600.png'
text = pytesseract.image_to_string(Image.open(filename), lang='deu')




# clean text

# strip stupid OCR bullshit results
p = re.compile('[A-Z ]+\n')
text = p.sub("",text)

# strip multiple new lines
p = re.compile('\n+')
text = p.sub("\n",text).strip()

