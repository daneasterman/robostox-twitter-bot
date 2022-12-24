import requests
import json
from bs4 import BeautifulSoup
from dateutil.parser import parse
from helpers.forms import FORMS
from helpers.sec_utils import *
from pprint import pprint
# @app.task
def get_tsla_filing():
	SEC_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=40&output=atom"
	# TSLA_ZEROS_CIK = "0001318605"
	CIK_TEST = "0000850261"
	headers = {'User-agent': 'Mozilla/5.0'}	
	try:
		response = requests.get(SEC_URL, headers=headers)
		soup = BeautifulSoup(response.content, "xml")
		filings = soup.findAll('entry')		
		for f in filings:
			title = f.title.text
			form_type = f.category.get("term")
			api_date = f.updated.text
			python_date = parse(api_date)
			human_date = python_date.strftime("%A, %B %d %Y at %I:%M%p (New York Time)")
			cik, filing_entity = circle_brackets_data(title)			
			filing = {
				"company_name": get_company_name(title),					
				"filing_link": f.link.get("href"),
				"form_type": form_type,
				"api_date": api_date,				
				"human_date": human_date,							
				"form_explanation": generate_form_explanation(form_type),
			}
			if filing_entity != "Reporting":
				if cik == CIK_TEST and form_type in FORMS.keys():
					# insert twitter func here
					print(filing)
				else:
					print("Incorrect cik and form skipped")
					continue				
			else:				
				print("Reporting entity skipped")
				continue			
	except Exception as e:
		print(f'The scraping job failed. See exception: {e}')

if __name__ == "__main__":
	get_tsla_filing()


