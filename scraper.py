#!/usr/bin/python3
import urllib.request, urllib.error, urllib.parse
import re

jw_spam = "https://joewein.net/dl/bl/dom-bl.txt"
response = urllib.request.urlopen(jw_spam)
raw_bl = response.read().decode("utf-8")
blacklist = raw_bl.split("\n")
for x in blacklist:
	print(re.sub(r"\;\d+", "",x))