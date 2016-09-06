import praw
from base64 import b64encode
from urllib import response
from bs4 import BeautifulSoup
from xml.sax.saxutils import unescape
from mal_bot_config import *
from mal_bot_funcs import *

# Log in to Reddit
r = praw.Reddit(user_agent=USER_AGENT)
r.login(USERNAME, PASSWORD)

