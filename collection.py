from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
from datetime import datetime
import time
import requests
import matplotlib.pyplot as plt
import os
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

log_dir = "Old"
right_engaging_words = [
    'trump', 'conservative', 'republican', 'right-wing', 'putin', 'haley',
    'mcconnell', 'gop', 'nra', 'tax cuts', 'pro-life', 'second amendment',
    'border wall', 'deportation', 'fox news', 'breitbart', 'libertarian',
    'school choice', 'deregulation', 'states\' rights', 'patriot',
    'nationalism', 'capitalism', 'traditional values', 'military',
    'law and order', 'blue lives'
]

left_engaging_words = [
    'biden', 'democrat', 'liberal', 'left-wing', 'sanders', 'aoc', 'pelosi',
    'progressive', 'green new deal', 'medicare for all', 'black lives matter',
    'antifa', 'climate change', 'gun control', 'pro-choice',
    'immigration reform', 'cnn', 'nytimes', 'universal healthcare',
    'minimum wage', 'lgbtq rights', 'social justice', 'defund the police',
    'tax the rich', 'free college', 'universal basic income', 'equality',
    'diversity'
]


def process_headlines(logs_dir='./aux/Old', alignment_dir='./alignment'):

  for filename in os.listdir(logs_dir):
    if filename.startswith("LOG_"):
      process_file(logs_dir, alignment_dir, filename)


def process_file(logs_dir, alignment_dir, filename):

  left_filename = os.path.join(alignment_dir,
                               f"LEFT_{filename.split('_', 1)[1]}")
  right_filename = os.path.join(alignment_dir,
                                f"RIGHT_{filename.split('_', 1)[1]}")

  with open(os.path.join(logs_dir, filename), 'r') as file:
    headlines = file.readlines()

  left_headlines = []
  right_headlines = []

  for headline in headlines:
    if any(word.lower() in headline.lower() for word in left_engaging_words):
      left_headlines.append(headline)
    if any(word.lower() in headline.lower() for word in right_engaging_words):
      right_headlines.append(headline)

  if left_headlines:
    with open(left_filename, 'w') as left_file:
      left_file.writelines(left_headlines)

  if right_headlines:
    with open(right_filename, 'w') as right_file:
      right_file.writelines(right_headlines)


if __name__ == "__main__":
  process_headlines()
