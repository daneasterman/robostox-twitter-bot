timestamp = datetime.now().strftime('%H:%M:%S-%Y-%m-%d')
	filename = 'articles-{}.json'.format(timestamp)
	with open(f"json/{filename}", 'w') as outfile:
		json.dump(entry_list, outfile)