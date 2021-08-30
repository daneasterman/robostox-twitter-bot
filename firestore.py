import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dateutil.parser import parse
import json

cred = credentials.Certificate('firestore-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
entries_ref = db.collection("entries")

breakpoint()

# READ OPERATION WORKINGS:

latest_query = entries_ref.order_by("python_date", direction=firestore.Query.DESCENDING).limit(1)
latest_docs = latest_query.get()
latest_db_list = [doc for doc in latest_docs]
latest_db_obj = latest_db_list[0].to_dict()


# with open('firestore_test.json', 'w') as outfile:
# 	json.dump(doc_list, outfile, indent=4)


