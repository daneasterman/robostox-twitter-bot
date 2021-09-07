import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dateutil.parser import parse
import json

cred = credentials.Certificate('firestore-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
entries_ref = db.collection("entries")

# breakpoint()

query_latest_entry = entries_ref.order_by(
	"python_date", direction=firestore.Query.DESCENDING).limit(1)
latest_results = query_latest_entry.get()
latest_db_list = [doc for doc in latest_results]
latest_db_pydate = latest_db_list[0].get("python_date")
latest_db_title = latest_db_list[0].get("title")
print("**LATEST FILING", latest_db_title)

query_earlier_entries = entries_ref.where("python_date", "<", latest_db_pydate)
earlier_results = query_earlier_entries.get()
for doc in earlier_results:
	print(doc.to_dict().get("title"))

# batch = db.batch()
# for doc in earlier_results:
# 	batch.delete(doc.reference)
# batch.commit()

# print('NUMBER OF EARLIER RESULTS', len(earlier_results))

# for doc in earlier_results:
# 	print("EARLIER RESULT TITLE:", doc.to_dict().get("title"))

# cities_ref = db.collection("cities")
# query = cities_ref.where("population", ">", 2500000).order_by("population").limit(2)
# results = query.stream()

# docs = db.collection(u'cities').where(u'capital', u'==', True).stream()
# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')

# with open('firestore_test.json', 'w') as outfile:
# 	json.dump(doc_list, outfile, indent=4)

# Syntax for calling function:
# stock_data, stock_content = generate_stock_info(user_symbol)

# gen_ref = entries_ref.limit(1)
# gen_result = gen_ref.get()

# if not gen_result:
# 	print(True)
# else:
# 	print(False)

