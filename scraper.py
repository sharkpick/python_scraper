#!/usr/bin/python3
import urllib.request, urllib.error, urllib.parse
import re, time, os, glob
from urllib.request import Request, urlopen

def diff(yesterday, blacklist):
	return(list(set(yesterday) - (set(blacklist))))

def malbytes_pull():
	mal_bytes = "https://blog.malwarebytes.com/detection/domain/"
	mal_regex = re.compile('<li><a href="https://blog.malwarebytes.com/detections/.+?/">(.+?)</a></li>')
	req = Request(mal_bytes, headers={'User-Agent': 'Mozilla/5.0'})
	raw_bl = urlopen(req).read().decode('utf-8')
	return(mal_regex.findall(raw_bl))

def jw_spam():
	jw_spam = "https://joewein.net/dl/bl/dom-bl.txt"
	with urllib.request.urlopen(jw_spam) as response:
		raw_bl = response.read().decode("utf-8")
	raw_bl= re.sub(r"\;\d+", "", raw_bl)
	return(raw_bl.split("\n"))
# make a timestamp
ts = time.gmtime()
raw_ts = "/home/python_scraper/data/raw/raw-" +time.strftime("%Y%m%d", ts)
diff_ts = "/home/python_scraper/data/blacklists/bl-" +time.strftime("%Y%m%d", ts)
raw_list = glob.glob('/home/python_scraper/data/raw/*')
yesterday_bl = max(raw_list, key=os.path.getctime)
# make var blacklist
blacklist = set()
for x in jw_spam():
	blacklist.add(x)
for y in malbytes_pull():
	blacklist.add(y)
blacklist = list(blacklist)
blacklist.sort()
# write to file
with open(raw_ts, 'w') as f:
	for x in blacklist:
		f.write(x + "\n")
# grab var yesterday for diff
with open(yesterday_bl, 'r') as f:
	raw = f.read()
yesterday = raw.split("\n")
new_diff = diff(yesterday, blacklist)
new_diff.sort()
with open(diff_ts, 'w') as f:
	for x in new_diff:
		f.write(x + "\n")