import json
import tweepy
import sys
from pathlib import Path

config = {}

print("For the next two questions, you'll need an application from https://developer.twitter.com/apps to Tweet with.")
config["consumer_key"] = input("Enter your app's consumer key: ")
config["consumer_secret"] = input("Enter your app's consumer secret key: ")

auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
try:
	redirect_url = auth.get_authorization_url()
	print("Go to the following URL and input the verification code given.")
	print(redirect_url)
except tweepy.TweepError:
	print("Unable to get a request token. Did you configure a valid consumer key and secret?")
	sys.exit(1)
	
verification_token = input("Verification token: ")
	
# Use given verification token to obtain an access key and secret
try:
	access_tokens = auth.get_access_token(verification_token)
	config["access_token"] = access_tokens[0]
	config["access_secret"] = access_tokens[1]
except tweepy.TweepError:
	print("Unable to get access credentials. Did you enter an invalid verification token?")
	sys.exit(1)

formatted_config = json.dumps(config, indent = 4)
config_path = Path("./config.json")
config_path.write_text(formatted_config)

print("All done, enjoy!")