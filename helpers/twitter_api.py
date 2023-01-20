import os
import tweepy
from helpers.sec_utils import create_bitly_url
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

TWITTER_API_KEY = str(os.getenv('TWITTER_API_KEY'))
TWITTER_API_KEY_SECRET = str(os.getenv('TWITTER_API_KEY_SECRET'))
TWITTER_ACCESS_TOKEN = str(os.getenv('TWITTER_ACCESS_TOKEN'))
TWITTER_ACCESS_TOKEN_SECRET = str(os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
API = tweepy.API(auth)

def create_tweet(filing):
	# Create the short link here to avoid so many Bitly API requests:
	short_link = create_bitly_url(filing['filing_link'])
	filing_copy = f"""
		🚨 🗃️ **CLOUD TEST** New SEC Filing Alert! 🗃️ 🚨

		{filing['company_name']} filed Form {filing['form_type']} at {filing['pretty_time']} (NYC Time).
		
		({filing['form_explanation']})

		More SEC info here: {short_link}
		
		"""
	try:
		# print(filing_copy)
		API.update_status(filing_copy)
	except Exception as e:
		print("**CREATE_TWEET ERROR:", e)

# create_tweet()