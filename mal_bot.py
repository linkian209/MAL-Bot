import praw
import re
import os
import sys
from mal_bot_config import *
from mal_bot_funcs import *


# Log in to Reddit
r = praw.Reddit(user_agent=USER_AGENT)
r.login(USERNAME, PASSWORD, disable_warning=True)

submission = r.get_submission(submission_id='51lhtb')
submission.replace_more_comments(limit=None, threshold=0)

# Get replied to comments
replied_to = []
if not os.path.isfile("posts_replied_to.txt"):
    replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
       raw = f.read()
       replied_to = raw.split("\n")

# Check comments
for comment in submission.comments:
	searchForAnime(comment, replied_to)

# Move all replied comments into the log for future runs
with open("posts_replied_to.txt", "w") as f:
	for item in replied_to:
		f.write(item+"\n")