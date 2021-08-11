import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dateutil.parser import parse
import json

cred = credentials.Certificate('firestore-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
entries_ref = db.collection("entries")

descend_docs = db.collection("entries").order_by("python_date")
results = descend_docs.stream()
results_list = [r for r in results]
for re in results_list:
	print(re.to_dict().get("human_date"))

breakpoint()

last_docs_list = [doc for doc in descend_docs]
real_last_doc = last_docs_list[0].to_dict()

all_entries = db.collection("entries").order_by("python_date").stream()
entries_list = [ent for ent in all_entries]
for item in entries_list:
	dict_item = item.to_dict()
	# print(dict_item["human_date"])

breakpoint()

print("**LATEST ENTRY", latest_entry)

print("** Number of entry items:", len(entries_list))

print("**", latest_entry_pydate)
# print("TYPE", type(latest_entry_pydate))

# Python datetime:
# Secs: %S

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


