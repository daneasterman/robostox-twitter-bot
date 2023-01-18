import requests
from celery import Celery
from bs4 import BeautifulSoup
from dateutil.parser import parse
from helpers.forms import FORMS
from helpers.sec_utils import *
from helpers.github_json import check_github_json
from pprint import pprint

message_counter = 0

app = Celery('tasks')
app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'scrape-every-10-seconds': {
        'task': 'main.get_filing',
        'schedule': 10.0
    },
}

@app.task
def get_filing():
	global message_counter
	message_counter += 1
	print('**MESSAGE COUNTER**', message_counter)
	SEC_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=40&output=atom"
	# TSLA_CIK = "0001318605"
	DUMMY_CIK = "0000863110"
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
			pretty_time = python_date.strftime("%I:%M%p")
			cik, filing_entity = circle_brackets_data(title)			
			filing = {
				"company_name": get_company_name(title),					
				"filing_link": f.link.get("href"),
				"form_type": form_type,
				"pretty_time": pretty_time,
				"raw_datetime": api_date,
				"form_explanation": generate_form_explanation(form_type),
				"cik_code": cik
			}
			if filing_entity != "Reporting":
				if cik == DUMMY_CIK and form_type in FORMS.keys():
					check_github_json(filing)
				else:
					# print("Skip, incorrect cik and form_type")
					continue
			else:
				# print("Skip, incorrect reporting entity")
				continue
	except Exception as e:
		print(f'Error: {e}')

# if __name__ == "__main__":
# 	get_filing()