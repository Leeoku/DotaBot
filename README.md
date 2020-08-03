![Alt text](/dotabotlogo.png "Title")

# DotaBot, a Dota Discord Bot

A personal Discord bot to work with my first API, Discord. This bot can help generate links, register users and create simple profiles

## Features
* `!hero` to get Dotabuff links and DotaWiki links for your hero
* `!register` to create a profile on the bot's database
* `!addhero/!delhero` to add/remove heroes from your top 5 list
* `!myprofile` to show your top 5 heroes

## Quickstart

This bot only runs in linux based systems due to a package called uvloop

Get your own discord bot token following a guide such as <a href = 'https://www.writebots.com/discord-bot-token/'>this</a>
* Update your discord bot token in /helpers/api_key.py


To connect to your own mongo connection, create your own cluster and database
* Update line 7, 9 of /helpers/dbase.py to your own cluster & database
* Update your mongo client connection in /helpers/api_key.py

To run the bot
* Ensure python 3 is installed 
* Create a virtual environment and start it
* pip install -r requirements.txt
* Change directory to project
* python3 main.py

## Technologies
* Python 3
* <a href = 'https://discordpy.readthedocs.io/en/latest/'>Discord.py</a>

## Database
* MongoDB with pymongo

## Acknowledgements
Snapshot for doing a code review and introducing me to many helper functions
