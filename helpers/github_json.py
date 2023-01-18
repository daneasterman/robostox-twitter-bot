import os
import json
from dotenv import load_dotenv
from github import Github
from helpers.twitter_api import create_tweet
load_dotenv()

def load_github_json():
	GITHUB_PERSONAL_ACCESS_TOKEN = str(os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN'))
	github = Github(GITHUB_PERSONAL_ACCESS_TOKEN)
	repo = github.get_user().get_repo('robostox-json-filings')
	file = repo.get_contents("json/data.json")
	list_data = json.loads(file.decoded_content.decode('utf-8'))	
	return repo, file, list_data

def check_github_json(filing):
	_, _, list_data = load_github_json()		
	if filing not in list_data:
		print("Make JSON DB entry")
		update_github_json(filing)
	else:
		print("Skip, found in DB")			

def update_github_json(filing):
	repo, file, list_data = load_github_json()
	list_data.append(filing)
	bytes_data = json.dumps(list_data).encode('utf-8')
	try:
		repo.update_file(file.path, f"{filing['company_name']}", bytes_data, file.sha)
		create_tweet(filing)
	except Exception as e:
		print("Error:", e)