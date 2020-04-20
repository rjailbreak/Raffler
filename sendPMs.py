
## Run this after running Raffle.py
## Check to see that winners_usernames.py has the usernames of winners
## Use an account with "mail" permissions to send a modmail.

import praw
from tqdm import tqdm
try:
	from winners_usernames import winners
except ModuleNotFoundError:
	print("Cannot import the list of winners. Are you sure you ran the raffle code? Call it using python3 raffle.py. Falling back to a manual list of users.")
	# If you want to just send a PM enter the users in the following array, without u/ in comma separated usernames in quotes: eg: ["hello", "world"] would send a PM to u/hello and u/world
	winners = []

## Settings
client_id = ''
client_secret = ''
username = ''
password = ''
# Sending a PM as a subreddit needs the mail permission
subreddit='jailbreak'

# Message subject
message_sub = ''
# This is the message content. Paste the content inside the three double-quotes
message_body = """ """
##

print("Logging in.")
r = praw.Reddit(client_id=client_id, client_secret=client_secret, username=username, password=password, user_agent="PM Winners personal Modmail bot")
print(f"Logged in successfully as {r.user.me()}")


for winner in tqdm(winners):
	try:
		r.redditor(winner).message(message_sub, message=message_body, from_subreddit=subreddit)
		print(f"Sent message to u/{winner}")
	except:
		print(f"Failed sending to u/{winner}")