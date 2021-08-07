import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

CREDS = credentials.Certificate('rtdb-sdk.json')
DB_URL = 'https://robostox-a3e6d-default-rtdb.europe-west1.firebasedatabase.app/'
firebase_admin.initialize_app(CREDS, {'databaseURL': DB_URL})	

DB_REF = db.reference("/")
for e in entry_list:
	print(e["human_date"])
	DB_REF.child("entries").push({
		"company_name": e["company_name"],
		"human_date": e["human_date"],
		'timestamp': {'.sv': 'timestamp'}
	})

snapshot = entries_ref.order_by_child("timestamp").limit_to_last(1).get()
for key, value in snapshot.items():
	print("***", value['company_name'])