import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta, timezone

# datetime.datetime(2019, 12, 7, tzinfo=ZoneInfo("America/Los_Angeles")) 

now = datetime.now(timezone.utc)
hr_extra = timedelta(hours=1)
future_date_time = now + hr_extra
past_date_time = now - hr_extra
# breakpoint()

cred = credentials.Certificate('firestore-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
entries_ref = db.collection("entries")

# New Filing - to delete periodically:
# lonestar_filing = {
# 	"title": "4 - Lonestar Resources US Inc. (0001661920) (Issuer)",
# 	"filing_link": "https://www.sec.gov/Archives/edgar/data/1661920/000089924321039526/0000899243-21-039526-index.htm",
# 	"form_type": "4",
# 	"api_date": "2021-10-06T11:23:00-04:00",
# 	"python_date": future_date_time,
# 	"human_date": "Wednesday, October 06 2021 at 11:23AM (New York Time)",
# 	"company_name": "Lonestar Resources US Inc.",
# 	"cik_code": "0001661920",
# 	"form_explanation": "Form 4 provides details on the buying or selling of stock by company insiders.",
# }
# try:
# 	entries_ref = db.collection("entries")
# 	entries_ref.add(lonestar_filing)
# 	print("lonestar_filing added!")
# except Exception as e:
# 	print(f"Error when trying to add to Firestore DB: {e}")

lightning_filing = {
	"title": "4 - Lightning eMotors, Inc. (0001802749) (Issuer)",
	"filing_link": "https://www.sec.gov/Archives/edgar/data/1661920/000089924321039526/0000899243-21-039526-index.htm",
	"form_type": "4",
	"api_date": "2021-10-06T11:23:00-04:00",
	"python_date": future_date_time,
	"human_date": "Wednesday, October 06 2021 at 11:23AM (New York Time)",
	"company_name": "Lightning eMotors, Inc.",
	"cik_code": "0001802749",
	"form_explanation": "Form 4 provides details on the buying or selling of stock by company insiders.",
}
try:
	entries_ref = db.collection("entries")
	entries_ref.add(lightning_filing)
	print("lightning_filing added!")
except Exception as e:
	print(f"Error when trying to add to Firestore DB: {e}")	

