![Alt text](/dotabotlogo.png "Title")

# DotaBot, a Dota Discord Bot

A personal Discord bot to work with my first API, Discord. This bot can help generate links, register users and create simple profiles

## Features
* `!hero` to get Dotabuff links and DotaWiki links for your hero
* `!register` to create a profile on the bot's database
* `!addhero/!delhero` to add/remove heroes from your top 5 list
* `!myprofile` to show your top 5 heroes

## Quickstart

The environment is containerized in Docker. To run the bot using Docker
* update /docker-compose.yml
* run `docker-compose up --build `

## Technologies
* Python 3
* <a href = 'https://discordpy.readthedocs.io/en/latest/'>Discord.py</a>
* Docker

## Database
* MongoDB with pymongo

## Acknowledgements
Snapshot for doing a code review and introducing me to many helper functions
