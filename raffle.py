import praw
from tqdm import tqdm
import datetime

# Check to check if the comment is "Load more comments" or "Continue this thread" link
from praw.models import MoreComments


#####
## MODIFY THE FOLLOWING SETTINGS
#####

no_of_winners = 150
post_url = ''
client_id = ''
client_secret = ''

##
# Year, month, date, hour, minute, seconds (don't put zero before the digits)
threshold_age = int(datetime.datetime(2020,1,1,0,0,0).timestamp())

winner_filename = "winners.txt"
winner_filename_csv = "winners_usernames.txt"
winner_filename_pm = "winners_usernames.py"

# Users to exclude. By default it excludes all moderators. Add more names in the array below as comma separated quoted strings. Eg:
# users_to_exclude = ["hello", "world"] will exclude u/Hello and u/world from winning apart from the moderators.
users_to_exclude = []


#####
## END OF SETTINGS. HERE BE DRAGONS.
#####


class account:
    def __init__(self, author, account_time, comment_body, comment_id):
        self.author = author
        self.account_time = account_time
        self.comment_body = comment_body
        self.comment_id = comment_id

reddit = praw.Reddit(user_agent='Random Raffle', client_id=client_id, client_secret=client_secret)

# Excluding moderators
for moderator in reddit.subreddit('jailbreak').moderator():
    users_to_exclude.append(moderator.name)

# Get the post
submission = reddit.submission(url=post_url)

top_level_comments = []
# This array will keep track of users already entered and will exclude multiple entries
users_already_seen = []
# Look at all top level comments and create class objects
submission.comments.replace_more(limit=None)
for top_level_comment in tqdm(submission.comments,desc="Downloading comments"):
    # Omit all load more comments objects
    if isinstance(top_level_comment, MoreComments):
        continue
    # Store all top level comments except moderators and very young users
    # if top_level_comment.banned_by is not None:
    if top_level_comment.author not in users_to_exclude:
        if top_level_comment.author not in users_already_seen:
            try:
                if top_level_comment.author.created_utc < threshold_age:
                    top_level_comments.append(account(top_level_comment.author,top_level_comment.author.created_utc,top_level_comment.body, top_level_comment.id))
                else:
                    print(f"u/{top_level_comment.author}'s account is too young. Excluding.")
            except:
                continue
            users_already_seen.append(top_level_comment.author)
        else:
            print(f"u/{top_level_comment.author} has a duplicate comment. Excluding.")
    else:
        print(f"u/{top_level_comment.author} is a moderator. Excluding.")
# Now we randomly choose `no_of_comments`
if no_of_winners > len(top_level_comments):
    print("Everyones a winner!")

# Get a random sample of users to win the raffle
import random
winner_indices = random.sample(range(len(top_level_comments)), no_of_winners)


winning_usernames = []
winning_comment_links = []
for index in winner_indices:
    print(f"u/{top_level_comments[index].author} is a winner! They commented: \"{top_level_comments[index].comment_body}\"")
    winning_usernames.append(str(top_level_comments[index].author))
    winning_comment_links.append(post_url + top_level_comments[index].comment_id)
with open(winner_filename,"w") as f:
    f.write("Username|Comment Link\n")
    f.write(':--|:--\n')
    for uname,link in zip(winning_usernames, winning_comment_links):
        f.write(f"u/{uname}|[link]({link})\n")

with open(winner_filename_csv,"w") as c:
    for uname in winning_usernames:
        c.write(f"u/{uname}\n")

write_string = ''
with open(winner_filename_pm, "w") as w:
    for i in range(len(winning_usernames)):
        if i == len(winning_usernames)-1:
            write_string += "\"" + winning_usernames[i] + "\""
            break
        write_string += "\"" + winning_usernames[i] + "\", "
    w.write(f"winners = [" + write_string + "]\n")