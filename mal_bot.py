import praw
import re
import os
import sys
from pprint import pprint
from mal_bot_config import *
from mal_bot_funcs import *


# Log in to Reddit
r = praw.Reddit(user_agent=USER_AGENT)
r.login(USERNAME, PASSWORD, disable_warning=True)

submission = r.get_submission(submission_id='51lhtb')

# Get replied to comments
replied_to = []
if not os.path.isfile("posts_replied_to.txt"):
    replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
       raw = f.read()
       replied_to = raw.split("\n")
       #replied_to = filter(None, raw)

# Check comments
# We search for strings enclosed in [[here]]
regex = r'\[{2}(.+?)\]{2}'
for comment in submission.comments:
	# Don't reply to a comment we already serviced
	if(comment.id in replied_to):
		print('Already commented on id %s' % comment.id)
		continue
	
	# Get all the anime in a comment
	groups = re.findall(regex, comment.body)
	if(len(groups) != 0):
		str = ''
		for anime in groups:
			str = str + getAnimeStats(anime)
			str += '\n\n---\n\n'
		str += FOOTER
		# Try to reply to the comment
		try:
			comment.reply(str)
			print('Replied to comment %s.' % comment.id)
			replied_to.append(comment.id)
		except:
			e = sys.exc_info()[1]
			print('Error has occured: [%s]' % e)
	
# Move all replied comments into the log for future runs
with open("posts_replied_to.txt", "w") as f:
	for item in replied_to:
		f.write(item+"\n")