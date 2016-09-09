#---------------------------
# MAL Bot Functions
#---------------------------
import re
from base64 import b64encode
from urllib import request
from bs4 import BeautifulSoup
from xml.sax.saxutils import unescape
from difflib import SequenceMatcher
from mal_bot_config import *

# printList is a debugging function
def printList(list):
	str = '['
	for i in list:
		str = str + i + ', '
	str += ']'
	print(str)
	
# Get MAL info about an anime
def getAnimeStats(anime):
	# Format string to replace spaces with pluses
	formatted = anime.replace(' ','+')
	
	# Make Request
	req = request.Request('https://myanimelist.net/api/anime/search.xml?q='+formatted)
	req.add_header('Authorization','Basic %s' % b64encode(b'%s:%s' % (MAL_UN, MAL_PW)).decode('utf-8'))
	raw = request.urlopen(req)
	
	# Parse request into a better xml object
	xml = BeautifulSoup(unescape(raw.read().decode('utf-8')), 'xml')
	
	# Put the entry closest to the queried anime into a dict
	anime_details = {}
	for item in xml.find_all('entry'):
		# Find the closest match to the entered title, check between Japanese and English
		japanese_closeness = SequenceMatcher(None, anime.lower(), item.title.string.lower()).ratio()
		english_closeness = SequenceMatcher(None, anime.lower(), str(item.english.string).lower()).ratio()
		closeness = max(japanese_closeness, english_closeness)
		if(len(anime_details.keys()) is 0 or anime_details['closeness'] < closeness):
			anime_details['id'] = str(item.id.string)
			anime_details['closeness'] = closeness
			anime_details['name'] = str(item.title.string)
			anime_details['synopsis'] = item.synopsis.text
			anime_details['episodes'] = str(item.episodes.string)
			anime_details['type'] = str(item.type.string)
			anime_details['score'] = str(item.score.string)
			anime_details['english'] = str(item.english.string)
			anime_details['synonyms'] = str(item.synonyms.string)
			anime_details['status'] = str(item.status.string)
			anime_details['start_date'] = str(item.start_date.string)
			anime_details['end_date'] = str(item.end_date.string)
			anime_details['image'] = str(item.image.string)
		
	# Format Synopsis (remove [i] and [b] and add '>' after '\n\n')
	anime_details['synopsis'] = re.sub('\[/?i\]','*',anime_details['synopsis'])
	anime_details['synopsis'] = re.sub('\[/?b\]','**',anime_details['synopsis'])
	anime_details['synopsis'] = re.sub('\n\n','\n\n> ',anime_details['synopsis'])
	# Format Comment
	comment = '**[%s](%s)**\n\n' % (anime_details['name'], anime_details['image'])
	comment += '> %s\n\n' % anime_details['synopsis']
	comment += ' | |\n---|---\n'
	comment += '**English** | %s\n' % anime_details['english']
	comment += '**Synonyms** | %s\n' % anime_details['synonyms']
	comment += '**Type** | %s\n' % anime_details['type']
	comment += '**Episodes** | %s\n' % anime_details['episodes']
	comment += '**Score** | %s\n' % anime_details['score']
	comment += '**Status** | %s\n' % anime_details['status']
	comment += '**Start Date** | %s\n' % anime_details['start_date']
	comment += '**End Date** | %s\n\n' % anime_details['end_date']
	comment += '[Click here for the more information](http://myanimelist.net/anime/%s)' % anime_details['id']
	
	return comment
	