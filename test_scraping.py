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

# Step 1:
SEC_XML_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=40&output=atom"
HEADERS = {'User-agent': 'Mozilla/5.0'}
RESPONSE = requests.get(SEC_XML_URL, headers=HEADERS)
SOUP = BeautifulSoup(RESPONSE.content, "xml")

import re

def get_parenthesis_data():
	entries = SOUP.findAll('entry')
	entry_list = [] 
	for e in entries:
		title = e.title.text
		string_list = re.findall(r'\(.*?\)', title)
		cik = string_list[0].strip("()")
		filing_type = string_list[1].strip("()")
		if filing_type != "Reporting":
			print(filing_type)
			print(title)
			# print("CIK", cik)
			

get_parenthesis_data()

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

def primary_scraper():
	try:				
		entries = SOUP.findAll('entry')
		entry_list = []
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
		print(f'Number of scraped entries: {len(entry_list)}')
	except Exception as e:
		print(f'The scraping job failed. See exception: {e}')

# primary_scraper()

