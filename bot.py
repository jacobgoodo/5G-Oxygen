import json
import logging
import tweepy
import random
import sys
from time import sleep
from pathlib import Path

config_path = Path("./config.json")
if not config_path.is_file():
    print("Please run setup.py first to configure.")
    sys.exit(1)

with config_path.open() as configfile:
    config = json.load(configfile)

# Attempt to load state.
state_path = Path("./state.json")
try:
    with state_path.open() as statefile:
        state = json.load(statefile)
except:
    # It seems loading isn't possible. Perhaps the user just set up our bot.
    # We'll start anew, with 5g being the first thing tweeted.
    state = {} 

auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
# Use our stored account credentials to authenticate.
auth.set_access_token(config["access_token"], config["access_secret"])

t = tweepy.API(auth)
if state == {}:
    print("About to tweet 5g initially. Please quit if this is not intended.")
    sleep(5)
    status = t.update_status("5g")
    state = {"last_tweet": status.id_str, "was_5g": True}

# Get the authenticated user's username, and keep it for repeated usage.
screen_name = t.me().screen_name

# You never know when the API and therefore your whole bot dies :p
while True:
    try:
        # Send a tweet with our current message, and a retweet of the previous one.
        # We retweet by linking to previous in the format https://twitter.com/username/status/id
        last_id = state["last_tweet"]
        link = f"https://twitter.com/{screen_name}/status/{last_id}"
        
        was_5g = state["was_5g"]
        if was_5g:
            content = "oxygen"
        else:
            content = "5g"

        tweet = f"{content} {link}"
        status = t.update_status(tweet)
        
        # Inverse the previous value, so that we can alternate next time.
        was_5g = not was_5g
        state = {"last_tweet": status.id_str, "was_5g": was_5g}
        
        # Write state to file.
        formatted = json.dumps(state, indent = 4)
        state_path.write_text(formatted)
        
        # Sleep for a random amount of time between 10min and 17min
        # This prevents spam and helps keep our rate limits low low low 🦀 (TM)
        sleep(random.randint(600, 1080))
        
    # Catch all exceptions.
    except Exception as e:
        print(f"An error occurred, continuing: {str(e)}")
        pass