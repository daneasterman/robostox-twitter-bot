from celery import Celery
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import json
import pprint
# pprint.pprint(entry_list)

# app = Celery()
# app.conf.timezone = 'UTC'

# app.conf.beat_schedule = {
#     'scrape-every-5-seconds': {
#         'task': 'tasks.get_rss',
#         'schedule': 5.0
#     },
# }

SEC_XML_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=40&output=atom"

FORMS = {
	"10-Q": "The 10-Q form is the quarterly report for the company. This form includes details on profit/loss, the balance sheet and cash flow. The company CEO or CFO will present these quarterly results in a conference call to investors and analysts.",
	"10-K": "The 10-K form is the annual financial report for the company.",
	"3": "Form 3 provides details on the buying or selling of stock by company insiders.",
	"4": "Form 4 provides details on the buying or selling of stock by company insiders.",
	"5": "Form 5 provides details on the buying or selling of stock by company insiders.",
	"8K": "Form 8-K reports on hiring/firing changes or other major structural changes in the company. For example this can include events such as: the resignation of the CFO, merger/acquisition announcements, or notifying investors of a new share buyback scheme.",
	"S-4": "Form S-4 includes details on the terms of a merger/acquisition deal.",
	"13D": "Form 13D is filed with the SEC when a person or group acquires more than 5 percent of the company's shares."
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

def save_function(entry_list):	
	entries_ref = db.collection("entries")
	# *** MAKE SURE THERE ARE DB ENTRIES BEFORE RUNNING BELOW:
	# latest_query = db.collection("entries").order_by("python_date", direction=firestore.Query.DESCENDING).limit(1)
	# latest_results = latest_query.get()
	# latest_db_list = [doc for doc in latest_results]
	# latest_db_obj = latest_db_list[0].to_dict()
	# latest_db_pydate = latest_db_obj.get("python_date")
	# latest_db_title = latest_db_obj.get("title")

	new_count = 0
	# print(f"**Latest article published: {latest_db_pydate}")
	for e in entry_list:
		# scraped_pydate = e["python_date"]
		# scraped_title = e["title"]
		# if scraped_pydate > latest_db_pydate or (scraped_pydate == latest_db_pydate and scraped_title != latest_db_title):
		try:
			new_count += 1
			entries_ref.add(e)
			print(f"Entry created for: {e['company_name']}")
		except Exception as e:
			print("Error when trying to add to Firestore DB:")
			print(e)
			break
	else:
		print("No new entries found")
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
			human_date = python_date.strftime("%A, %B %d %Y at %I:%M%p")
			
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
		
		print('Finished scraping entries')
		print('** NUMBER OF ENTRIES', len(entry_list))
		return save_function(entry_list)

	except Exception as e:
		print('The scraping job failed. See exception: ')
		print(e)

get_rss()





