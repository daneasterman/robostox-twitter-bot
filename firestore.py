import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dateutil.parser import parse
import json

cred = credentials.Certificate('firestore-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
entries_ref = db.collection("entries")

docs = db.collection("entries").order_by("created_at").limit(1).get()
latest_entry_list = [doc for doc in docs]
latest_entry = latest_entry_list[0].to_dict()
latest_entry_pydate = parse(latest_entry.get("api_date"))

print("**", latest_entry_pydate)
print("TYPE", type(latest_entry_pydate))



# with open("json/simple.json") as file:
# 	data_entries = json.load(file)
# 	for e in data_entries:
# 		entries_ref.add({
# 			"company_name": e["company_name"],
# 			"human_date": e["human_date"],
# 			"created_at": firestore.SERVER_TIMESTAMP
# 		})

# PROOF OF CONCEPT - READ:

# cred = credentials.Certificate('firestore-sdk.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# docs = db.collection("entries").order_by("created_at").limit(5).get()
# doc_list = []

# for doc in docs:
# 	print(doc.to_dict()["company_name"])
# 	doc_list.append({
# 	"company_name": doc.to_dict()["company_name"],
# 	"human_date": doc.to_dict()["human_date"]
# 	})

# with open('firestore_test.json', 'w') as outfile:
# 	json.dump(doc_list, outfile, indent=4)


