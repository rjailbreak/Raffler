# Raffle

Login and choose comments randomly from a thread. By default excludes all moderators, and duplicate comments by the same user. Supports excluding specific users too.

Completely configurable with the following parameters:

1. `no_of_winners` - The number of winners to choose
2. `post_url` - The url of the post to pull winners from
3. `threshold_age` - The age of the user account. Accounts younger than this are excluded from winning.
4. `winner_filename` - Create a text file with usernames of the winners and a permalink to their comment nicely formatted for a Reddit post.
5. `winner_filename_csv` - Only output the usernames of the winners to a text file
6. `winner_filename_pm` - A python compatible string that is read by `sendPMs.py` to send modmails to the winners
7. `users_to_exclude` - A python list with the names of users who need to be excluded. For instance setting it to say ["hello", "world"] will exclude u/Hello and u/world from winning apart from the moderators.

## Setup
  
Create a new script application in your reddit account [here](https://old.reddit.com/prefs/apps/) and note down the `client_id` and `client_secret`

Paste these values in the `raffle.py` file within the quotes.

Also do this for `sendPMs.py` to authenticate and send modmails. Ensure that you have mail permissions to send a modmail.

## Running

1. `cd` to the project folder Install dependencies by using `pip3 install -r requirements.txt`.
2. Run `raffle.py` using `python3 raffle.py`
3. Verify that the users in `winner_usernames.py` and `winner_usernames.txt` all match.
4. Open `sendPMs.py` to customize the modmail message and subject. You need to enter the credentials of a user/moderator with the mail permissions. (Follow the setup as above. If you already used a moderator account for the giveaway, you can reuse the credentials here.)
5. Run `python3 sendPMs.py` to send a modmail to the user with the message.


## Requirements

praw==6.5.1
tqdm==4.43.0
