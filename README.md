# MAL Bot

A Reddit bot that will look through /r/anime for comments containing a formatted string and will reply with 
a overview of the anime that has been linked in the formatted string. It will also pull from the user's MAL
using the flair text and get the user's personal score and comments about the anime.

## Required Packages
* lxml = 3.6.4
* BeautifulSoup = 4.4.1
* praw >= 3.5.0

## Setup
In order to setup the bot, you must fill in information for the bot in the mal_bot_skel.py file. The save a copy of the file as mal_bot_config.py. 

## Invoking

To invoke the bot, simply enclose the anime (Japanese or English title) in double brackets:
* [[Naruto]]
* [[Erased]]
* [[Shokugeki no Soma]]

## License
Licensed under the MIT License 2.0 