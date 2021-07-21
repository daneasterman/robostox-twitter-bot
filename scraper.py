import requests
import sys
from bs4 import BeautifulSoup
import urllib.request


# scraping function
# hacker_url = "https://news.ycombinator.com/rss"

sec_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=40&output=atom"

# scraping function
def hackernews_rss():	
	headers = {'User-agent': 'Mozilla/5.0'}
	try:		
		r = requests.get(sec_url, headers=headers)
		soup = BeautifulSoup(r.content, "xml")		
		print(soup)

	except Exception as e:
		print('The scraping job failed. See exception: ')
		print(e)

hackernews_rss()


