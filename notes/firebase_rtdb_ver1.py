import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

cred = credentials.Certificate('rtdb-sdk.json')
DB_URL = 'https://robostox-a3e6d-default-rtdb.europe-west1.firebasedatabase.app/'

firebase_admin.initialize_app(cred, {
    'databaseURL': DB_URL
})

DB_REF = db.reference("/")

entries = [{
		"filing_link": "https://www.sec.gov/Archives/edgar/data/1767339/000176733921000006/0001767339-21-000006-index.htm",
		"form_type": "D",
		"form_explanation": "",
		"human_date": "Tuesday, August 03 2021 at 10:50AM",
		"company_name": "HELLO TEST",
		"cik_code": "001767339"
},
{
		"filing_link": "https://www.sec.gov/Archives/edgar/data/1767339/000176733921000006/0001767339-21-000006-index.htm",
		"form_type": "D",
		"form_explanation": "",
		"human_date": "Tuesday, August 03 2021 at 10:50AM",
		"company_name": "HELLO TEST",
		"cik_code": "001767339"
}]

with open("json/simple.json") as file:
	data = json.load(file)
	for e in data:
		DB_REF.child("entries").push(e)
	
