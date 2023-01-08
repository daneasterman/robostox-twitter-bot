import os
import tweepy
from helpers.sec_utils import create_bitly_url
from dotenv import load_dotenv
load_dotenv()

TWITTER_API_KEY = str(os.getenv('TWITTER_API_KEY'))
TWITTER_API_KEY_SECRET = str(os.getenv('TWITTER_API_KEY_SECRET'))
TWITTER_ACCESS_TOKEN = str(os.getenv('TWITTER_ACCESS_TOKEN'))
TWITTER_ACCESS_TOKEN_SECRET = str(os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

def create_tweet(filing):
	auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
	auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
	API = tweepy.API(auth)
	# Create the short link here to avoid so many Bitly API requests:
	short_link = create_bitly_url(filing['filing_link'])
	filing_copy = f"""
		🚨 🗃️ **TEST** New SEC Filing Alert! 🗃️ 🚨

		{filing['company_name']} just filed Form {filing['form_type']} at {filing['human_time']} (NYC Time).
		
		{filing['form_explanation']}

		More SEC info here: {short_link}
		"""
	# Insert checking func here. 
	try:
		print(filing_copy)
		# API.update_status(filing_copy)
	except Exception as e:
		print("Error:", e)

# create_tweet()