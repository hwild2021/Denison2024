from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
from datetime import datetime
import time
import requests
import matplotlib.pyplot as plt
import os
import re

global sites
sites = []

global cutoff
cutoff = 30


class Site:

  def __init__(self,
               url,
               tag,
               category_func,
               class_="",
               container="",
               block=""):
    self.url = url
    self.tag = tag
    self.category = category_func
    self.txt = ""
    

    self.headlines = ""
    self.block = block
    self.class_ = class_
    self.container = container

    sites.append(self)

  def get_headlines(self):
    self.response = requests.get(self.url)
    self.soup = BS(self.response.text, 'html.parser')
    for category in self.category:
      category(self)

    self.save()

  def save(self):
    now = datetime.now()
    filename = str(self.tag + "_" + now.strftime("%d:%m:%Y_%H:%M:%S" + ".txt"))
    filename = "./logs/LOG_" + filename
    f = open(filename, 'x')
    f.write(self.txt)
    f.close()


def h3site(site):
  site.headlines = site.soup.find_all('h3')
  for headline in site.headlines:
    line = headline
    if line:
      line_text = line.get_text().strip()
      line_text_split = line_text.split('\n')
      for line_individual in line_text_split:
        if len(line_individual) > cutoff:
          site.txt = site.txt + line_individual + "\n"


def h4site(site):
  site.headlines = site.soup.find_all('h4')
  for headline in site.headlines:
    line = headline
    if line:
      line_text = line.get_text().strip()
      line_text_split = line_text.split('\n')
      for line_individual in line_text_split:
        if len(line_individual) > cutoff:
          site.txt = site.txt + line_individual + "\n"


def h2site(site):
  site.headlines = site.soup.find_all('h2')
  for headline in site.headlines:
    line = headline
    if line:
      line_text = line.get_text().strip()
      line_text_split = line_text.split('\n')
      for line_individual in line_text_split:
        if len(line_individual) > cutoff:
          site.txt = site.txt + line_individual + "\n"


def byclass(site):
  site.headlines = site.soup.find_all(class_=site.class_)
  for headline in site.headlines:
    if site.container != "":
      line = headline.find(site.block, class_=site.container)
    else:
      line = headline
    if line:
      line_text = line.get_text().strip()
      line_text_split = line_text.split('\n')
      for line_individual in line_text_split:
        if len(line_individual) > cutoff:
          site.txt = site.txt + line_individual + "\n"


fox = Site("https://www.foxnews.com/", "fox", [h3site], block="a")
smh = Site("https://www.smh.com.au", "smh", [h3site], block="a")
cnn = Site("https://www.edition.cnn.com/",
           "cnn", [byclass],
           class_="container__headline",
           container="container__headline-text",
           block="span")
msn = Site("https://www.msnbc.com/", "msn", [h2site], block="a")
skyus = Site("https://news.sky.com/us",
             "skyus", [byclass],
             class_="ui-story-headline",
             block="a")
nypost = Site("https://nypost.com/", "nypost", [h2site, h3site], block="a")
abcus = Site("https://abcnews.go.com/",
             "abcus", [h3site, byclass, h4site, h2site],
             class_="title card")
breit = Site("https://www.breitbart.com/", "breit", [h2site])
abcau = Site("https://www.abc.net.au/news",
             "abcau", [h3site, byclass],
             class_="ListItem",
             block="a")
newscom = Site("https://www.news.com.au/", "newscom", [h4site], block="a")
nine = Site("https://www.9news.com.au/", "nine", [h3site], block="a")
daily = Site("https://www.dailytelegraph.com.au/",
             "daily", [h4site],
             block="a")
nbc = Site("https://www.nbcnews.com/", "nbc", [h2site])

def extract_and_save_headlines():
  for site in sites:
      site.get_headlines()
      print(f"Extracted headlines for {site.tag}")

def run_every_hour():
  while True:
      extract_and_save_headlines()
      time.sleep(3600)

if __name__ == "__main__":
  run_every_hour()