""" Script to pull in gen7pu data """
import requests
import re


print("Here")
BASE_URL = "http://www.smogon.com/stats/2017-12/chaos/gen7pu-{}.json"
LEVELS = [0, 1500, 1630, 1760]

for level in LEVELS:
    print(level)
    raw_html = requests.get(BASE_URL.format(level)).content
    file_ = open("raw_data/gen7pu-{}.json".format(level), mode='wb')
    file_.write(raw_html)
    file_.close()

print("Done")