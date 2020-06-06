# DotaBot, a Dota Discord Bot

A personal Discord bot to work with my first API, Discord. This bot can help generate links, register users and create simple profiles

## Features
* `!hero` to get Dotabuff links and DotaWiki links for your hero
* `!register` to create a profile on the bot's database
* `!addhero/!delhero` to add/remove heroes from your top 5 list
* `!myprofile` to show your top 5 heroes

## Quickstart

```
Ensure python 3 is installed
python3 -m virtualenv
pip install -r requirements.txt
python3 main.py
```

## Technologies
* Python 3
* <a href = 'https://discordpy.readthedocs.io/en/latest/'>Discord.py</a> - Parsing the .doc file

## Database
* MongoDB with pymongo

## Acknowledgements
Snapshot for doing a code review and introducing me to many helper functions
