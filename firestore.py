import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

cred = credentials.Certificate('firestore-sdk.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
entries_ref = db.collection("entries")

with open("json/simple.json") as file:
	data_entries = json.load(file)
	for e in data_entries:
		entries_ref.add({
			"company_name": e["company_name"],
			"human_date": e["human_date"],
			"created_at": firestore.SERVER_TIMESTAMP
		})