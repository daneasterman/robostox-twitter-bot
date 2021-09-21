from celery import Celery
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

import json
import pprint
# pprint.pprint(entry_list)

app = Celery('tasks')
app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'scrape-every-5-seconds': {
        'task': 'tasks.get_rss',
        'schedule': 5.0
    },
}

SEC_XML_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=40&output=atom"

FORMS = {
	"10-Q": "The 10-Q form is the quarterly report for the company. This form includes details on profit/loss, the balance sheet and cash flow. The company CEO or CFO will present these quarterly results in a conference call to investors and analysts.",
	"10-K": "The 10-K form is the annual financial report for the company.",
	"3": "Form 3 provides details on the buying or selling of stock by company insiders.",
	"4": "Form 4 provides details on the buying or selling of stock by company insiders.",
	"5": "Form 5 provides details on the buying or selling of stock by company insiders.",
	"8K": "Form 8-K reports on any major unscheduled event at the company. For example this can include: hiring/firing important executives, resignations, merger/acquisition announcements, or notifying investors of a new share buyback scheme.",
	"S-4": "Form S-4 includes details on the terms of a merger/acquisition deal.",
	"13D": "Form 13D is filed with the SEC when a person or group acquires more than 5 percent of a company's shares.",
	"13G": "Form 13G is a shorter version of Form 13D which is filed with the SEC when a person or group acquires more than 5 percent of a company's shares.",
	"425": "Form 425 is a prospectus document disclosing information on a business combination such as a merger."
}

def get_company_name(title):
	start_name = title.index(" - ") +3
	end_name = title.index("(") -1
	company_name = title[start_name:end_name]
	return company_name

def get_cik(title):
	start_cik = title.index("(") +2
	end_cik = title.index(")")
	cik_code = title[start_cik:end_cik]
	return cik_code

def generate_form_explanation(form_type):
	form_explanation = FORMS.get(form_type, "")
	return form_explanation

cred = credentials.Certificate('firestore-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_latest_entry(entries_ref):
	query_latest_entry = entries_ref.order_by(
			"python_date", direction=firestore.Query.DESCENDING).limit(1)
	latest_results = query_latest_entry.get()
	latest_db_list = [doc for doc in latest_results]
	latest_db_pydate = latest_db_list[0].get("python_date")
	return latest_db_pydate

def save_to_firestore(entry_list):
	# Setup variables:
	entries_ref = db.collection("entries")
	gen_ref = entries_ref.limit(1)
	gen_result = gen_ref.get()
	new_count = 0

	# Simply add entries with for loop if nothing in DB for first time:
	if not gen_result:
		for e in entry_list:
			try:
				new_count += 1
				entries_ref.add(e)				
				print(f"Entry created for: {e['company_name']}")
			except Exception as e:
				print(f"Error when trying to add to Firestore DB: {e}")	
				break	
	else:
		latest_db_pydate = get_latest_entry(entries_ref)	
		for e in entry_list:
			scraped_pydate = e["python_date"]			
			if scraped_pydate > latest_db_pydate:
				try:
					new_count += 1
					entries_ref.add(e)
					print(f"Entry created for: {e['company_name']}")
				except Exception as e:
					print(f"Error when trying to add to Firestore DB: {e}")
					break
			# Do the periodic delete here at end of the cycle:		
	print(f"New articles added to DB: {new_count}")

# @app.task
def get_rss():
	headers = {'User-agent': 'Mozilla/5.0'}	
	entry_list = []

	try:
		resp = requests.get(SEC_XML_URL, headers=headers)
		soup = BeautifulSoup(resp.content, "xml")
		entries = soup.findAll('entry')
		for e in entries:
			title = e.title.text
			filing_link = e.link.get("href")
			form_type = e.category.get("term")
			api_date = e.updated.text
			python_date = parse(api_date)
			human_date = python_date.strftime("%A, %B %d %Y at %I:%M%p (New York Time)")
			
			entry = {
				"title": title,
				"filing_link": filing_link,
				"form_type": form_type,
				"api_date": api_date,
				"python_date": python_date,
				"human_date": human_date,
				"company_name": get_company_name(title),
				"cik_code": get_cik(title),
				"form_explanation": generate_form_explanation(form_type),
			}
			entry_list.append(entry)		
		
		print('**Number of scraped entries:', len(entry_list))
		return save_to_firestore(entry_list)

	except Exception as e:
		print(f'The scraping job failed. See exception: {e}')		

get_rss()





