#---------------------------
# MAL Bot Functions
#---------------------------
import re
import praw
import string
from base64 import b64encode
from urllib import request
from bs4 import BeautifulSoup
from xml.sax.saxutils import unescape
from difflib import SequenceMatcher
from mal_bot_config import *

# Status Dict for User info
STATUS = {'1': 'Watching', '2': 'Completed', '3': 'On-Hold', '4': 'Dropped', '5': 'Plan to Watch'}

# printList is a debugging function
def printList(list):
	str = '['
	for i in list:
		str = str + i + ', '
	str += ']'
	print(str)

# Split the name up and try to get a better match for an anime
def splitNameAndGetStats(anime):
	split_name = anime.split()
	anime_details = {}
	for name in split_name:
		# Make Request
		req = request.Request('https://myanimelist.net/api/anime/search.xml?q='+name)
		req.add_header('Authorization','Basic %s' % b64encode(b'%s:%s' % (MAL_UN, MAL_PW)).decode('utf-8'))
		raw = request.urlopen(req)
	
		# Parse request into a better xml object
		xml = BeautifulSoup(unescape(raw.read().decode('utf-8')), 'xml')
	
		# Put the entry closest to the queried anime into a dict
		punct = re.compile('[%s]' % re.escape(string.punctuation))
		for item in xml.find_all('entry'):
			# Find the closest match to the entered title, check between Japanese and English
			japanese_closeness = SequenceMatcher(None, re.sub(punct,' ',anime.lower()), re.sub(punct,' ',item.title.string.lower())).ratio()
			english_closeness = SequenceMatcher(None, re.sub(punct,' ',anime.lower()), re.sub(punct,' ',str(item.english.string).lower())).ratio()
			closeness = max(japanese_closeness, english_closeness)
			if(len(anime_details.keys()) is 0 or anime_details['closeness'] < closeness):
				try:
					print('old closeness: {}'.format(anime_details['closeness']))
					print('old name: {}'.format(anime_details['name']))
				except:
					print('')
				print('new closeness: {}'.format(closeness))
				print('new name: {}'.format(str(item.title.string)))
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
				
	# Return the details
	return anime_details
	
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
	punct = re.compile('[%s]' % re.escape(string.punctuation))
	for item in xml.find_all('entry'):
		# Find the closest match to the entered title, check between Japanese and English
		japanese_closeness = SequenceMatcher(None, re.sub(punct,' ',anime.lower()), re.sub(punct,' ',item.title.string.lower())).ratio()
		english_closeness = SequenceMatcher(None, re.sub(punct,' ',anime.lower()), re.sub(punct,' ',str(item.english.string).lower())).ratio()
		closeness = max(japanese_closeness, english_closeness)
		if(len(anime_details.keys()) is 0 or anime_details['closeness'] < closeness):
			try:
				print('old closeness: {}'.format(anime_details['closeness']))
				print('old name: {}'.format(anime_details['name']))
			except:
				print('')
			print('new closeness: {}'.format(closeness))
			print('new name: {}'.format(str(item.title.string)))
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
			
	# If the final closeness isn't good enough, break anime name up and try for a closer match.
	if anime_details['closeness'] < MIN_ACCEPTABLE_CLOSENESS:
		anime_details = splitNameAndGetStats(anime)
	
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
	
	return (comment, anime_details)

# Get User Statistics on the inputted anime
def getCommentorStats(anime_details, list_url):
	# If they don't have a flair, return nothing
	if(list_url is ''):
		return ''
	
	# Make sure the list is from MAL
	if 'myanimelist' in list_url:
		# Get the user's username
		username = list_url.split('/animelist/')[1]
		
		# Now create the request
		url = 'http://myanimelist.net/malappinfo.php?u=' + username + '&status=all&type=anime'
		req = request.Request(url)
		raw = request.urlopen(req)
		
		# Begin decoding and get the anime
		xml = BeautifulSoup(unescape(raw.read().decode('utf-8')), 'xml')
		comment = ''
		
		for anime in xml.find_all('anime'):
			# Check if this is the current
			if int(anime.series_animedb_id.text) == int(anime_details['id']):
				# Format the comment to return
				comment = '\n\nPersonal Statistics \n\n'
				comment += ' | |\n---|---\n'
				comment += '**Score** | %s\n' % anime.my_score.text
				comment += '**Status** | %s\n' % STATUS[anime.my_status.text]
				comment += '**Completed Episodes** | %s\n\n' % anime.my_watched_episodes.text
				break
				
		# If the show isn't on the user's MAL, let them know
		if comment == '':
			comment = '\n\nThis anime is not the list of %s!' % username
		
		return comment
		
# Recursively go through comments and replies to search for anime
def searchForAnime(comment, replied_to):
	if isinstance(comment, praw.objects.Comment):
		# We search for strings enclosed in [[here]]
		regex = r'\[{2}(.+?)\]{2}'
		
		# Don't reply to a comment we already serviced
		if(comment.id in replied_to):
			print('Already commented on id %s' % comment.id)
		
		# Get all the anime in a comment
		else:
			groups = re.findall(regex, comment.body)
			if(len(groups) != 0):
				str = ''
				for anime in groups:
					stats, anime_details = getAnimeStats(anime)
					str = str + stats
					str = str + getCommentorStats(anime_details, comment.author_flair_text)
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
					
		# If there are replies, loop through them
		for reply in comment.replies:
			searchForAnime(reply, replied_to)