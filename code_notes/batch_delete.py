def delete_earlier_entries(entries_ref, latest_db_pydate):
	batch = db.batch()
	query_earlier_entries = entries_ref.where("python_date", "<", latest_db_pydate)
	earlier_results = query_earlier_entries.get()
	time.sleep(10)
	for doc in earlier_results:
		print('Deleting:', doc.to_dict().get("title"))	
		batch.delete(doc.reference)
	batch.commit()