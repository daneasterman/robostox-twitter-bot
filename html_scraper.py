import requests
from bs4 import BeautifulSoup
import json

SEC_XML_URL="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&output=atom&CIK=PYPL"

def get_xml():
	headers = {'User-agent': 'Mozilla/5.0'}
	
	try:		
		resp = requests.get(SEC_XML_URL, headers=headers)
		soup = BeautifulSoup(resp.content, "xml")
		print(resp.status_code)
		print("**START SOUP", soup)
		# with open("json/DEBUG", 'w') as outfile:
		# 	json.dump(entry_list, outfile)		

	except Exception as e:
		print('The scraping job failed. See exception: ')
		print(e)

get_xml()