""" from selenium import webdriver
browser = webdriver.PhantomJS()
browser.get("https://www.baidu.com")
print(browser.current_url)
 """

import tesserocr
from PIL import Image
image = Image.open('image.png')
print(tesserocr.image_to_text(image))