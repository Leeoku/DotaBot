![Alt text](/dotabotlogo.png "Title")

# DotaBot, a Dota Discord Bot

A personal Discord bot to work with my first API, Discord. This bot can help generate links, register users and create simple profiles

<p><a href = 'https://www.loom.com/share/a7efdbe134d245a6a212e691213ef778'>Demo</a></p>
<p><a href = 'https://top.gg/bot/471769821546283049'>Invite to your Discord server!</a></p>

## Features
* `!hero` to get Dotabuff links and DotaWiki links for your hero
* `!register` to create a profile on the bot's database
* `!addhero/!delhero` to add/remove heroes from your top 5 list
* `!myprofile` to show your top 5 heroes

## Quickstart

#### Container instructions
* ```docker-compose up --build``` (first build)
* Afterwards, just ```docker-compose up```


#### Original instructions for local running

This bot only runs in linux based systems due to a package called uvloop. Recommend to use container

* Ensure python 3 is installed 
* Create a virtual environment and start it
* ```pip install -r requirements.txt```
* Change directory to project
* ```python3 main.py```



## Technologies
* Python 3
* <a href = 'https://discordpy.readthedocs.io/en/latest/'>Discord.py</a>

## Database
* MongoDB with pymongo

## Acknowledgements
Snapshot for doing a code review and introducing me to many helper functions
