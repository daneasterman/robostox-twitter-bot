import requests
import sentry_sdk
from celery import Celery
from bs4 import BeautifulSoup
from dateutil.parser import parse
from helpers.forms import FORMS
from helpers.sec_utils import *
from helpers.github_json import check_github_json
load_dotenv()

app = Celery('tasks')
app.conf.timezone = 'UTC'
app.conf.broker_pool_limit = 1
app.conf.broker_url = os.getenv('CLOUDAMQP_URL')
app.conf.beat_schedule = {
    'scrape-every-10-seconds': {
        'task': 'main.get_filing',
        'schedule': 10.0
    },
}
sentry_sdk.init(os.getenv('SENTRY_DSN'))

@app.task
def get_filing():
	SEC_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=40&output=atom"
	TSLA_CIK = "0001318605"
	# DUMMY_CIK = "0001048477"
	user_agent = "RoboStox hellorobostox@gmail.com"
	headers = {'User-agent': user_agent}
	try:
		response = requests.get(SEC_URL, headers=headers)
		if response.status_code != 200:
			raise Exception(f"Status Code Error: {response.status_code}")
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
				if cik == TSLA_CIK and form_type in FORMS.keys():
					check_github_json(filing)
				else:						
					continue
			else:
				continue
	except Exception as e:
		sentry_sdk.capture_exception(e)

# if __name__ == "__main__":
# 	get_filing()