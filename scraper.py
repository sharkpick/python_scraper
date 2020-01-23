#!/usr/bin/python3
import urllib.request, urllib.error, urllib.parse
import re, time, os
from urllib.request import Request, urlopen

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
	raw_bl= re.sub(r"(:|\;)\d+", "", raw_bl)
	return(raw_bl.split("\n"))
def timestamp():
	global raw_ts, diff_ts, raw_list, err_check, raw_path
	home = '/opt/python_scraper'
	raw_path = home + "/data/raw/"
	ts = time.gmtime()
	raw_ts = home + "/data/raw/raw-" +time.strftime("%Y%m%d", ts)
	diff_ts = home + "/data/blacklists/bl-" +time.strftime("%Y%m%d", ts)
	raw_list = sorted(os.listdir(home + "/data/raw/"))
	err_check = int(len(raw_list)) # for later
# ok begin
timestamp()
blacklist = set()
for x in jw_spam():
	blacklist.add(x)
for x in malbytes_pull():
	blacklist.add(x)
blacklist = list(sorted(blacklist))
if err_check < 1:
	with open(raw_ts, 'w') as f:
		for x in blacklist:
			f.write(x + "\n")
	exit()
else:
	yesterday_bl = raw_path + raw_list[-1]
	with open(raw_ts, 'w') as f:
		for x in blacklist:
			f.write(x + "\n")
with open(yesterday_bl, 'r') as f:
	raw = f.read()
yesterday = raw.split("\n")
new_diff = set(blacklist) - set(yesterday)
new_diff = list(sorted(new_diff))
with open(diff_ts, 'w') as f:
	for x in new_diff:
		f.write(x + "\n")