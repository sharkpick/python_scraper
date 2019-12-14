#!/usr/bin/python3
import urllib.request, urllib.error, urllib.parse
import re, time, os, glob

# quick, grab last (new) raw BL, before we make any new files
raw_list = glob.glob('/home/will/data/raw/*')
yesterday_bl = max(raw_list, key=os.path.getctime)
#print(yesterday_bl) # debug
# make some timestamps
ts = time.gmtime()
raw_ts = "/home/will/data/raw/raw-" +time.strftime("%Y%m%d", ts)
diff_ts = "/home/will/data/blacklists/bl-" +time.strftime("%Y%m%d", ts)
# pull some domains
jw_spam = "https://joewein.net/dl/bl/dom-bl.txt"
with urllib.request.urlopen(jw_spam) as response:
	raw_bl = response.read().decode("utf-8")
blacklist = raw_bl.split("\n")
# write formatted domains to file
with open(raw_ts, "w") as f:
	for x in blacklist:
		f.write(re.sub(r"\;\d+", "",x) + "\n")
# find diff - get yesterday's BL
with open(yesterday_bl, "r") as f:
	raw = f.read()
yesterday = raw.split("\n")

def Diff(yesterday, blacklist):
	return(list(set(yesterday) - set(blacklist)))
new_diff = Diff(yesterday, blacklist)
new_diff.sort()
with open(diff_ts, "w") as f:
	for x in new_diff:
		f.write(x + "\n")