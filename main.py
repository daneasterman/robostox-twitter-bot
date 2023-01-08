import requests
from celery import Celery
from bs4 import BeautifulSoup
from dateutil.parser import parse
from helpers.forms import FORMS
from helpers.sec_utils import *
from twitter_api import create_tweet
from pprint import pprint

app = Celery('tasks')
app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'scrape-every-5-seconds': {
        'task': 'main.get_filing',
        'schedule': 5.0
    },
}

@app.task
def get_filing():
	SEC_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=40&output=atom"
	# TSLA_CIK = "0001318605"
	CIK_TEST = "0001318605"
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
			human_time = python_date.strftime("%I:%M%p")
			cik, filing_entity = circle_brackets_data(title)
			filing = {
				"company_name": get_company_name(title),					
				"filing_link": f.link.get("href"),
				"form_type": form_type,			
				"human_time": human_time,
				"form_explanation": generate_form_explanation(form_type),
			}			
			if filing_entity != "Reporting":
				if cik == CIK_TEST and form_type in FORMS.keys():
					create_tweet(filing)
					# print(filing)
				else:
					# print("Incorrect cik and form skipped")
					continue
			else:				
				# print("Reporting entity skipped")
				continue			
	except Exception as e:
		print(f'See exception: {e}')

# if __name__ == "__main__":
# 	get_filing()
