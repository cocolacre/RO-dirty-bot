# RO-dirty-bot
Simple and dirty mmorpg pixel bot project with an objective of running 24hrs unattended and generating small profit. 
I used this project to "succesfully" bot on Talonro and Novaro servers of Ragnarok Online mmorpg.
It has even generated some small profit.
The code is ugly and it was not meant to be published.
Most of the time it was used to bot on Novaro.
The setup for botting is folowwing:
-A rebellion 130lvl+ with a Tempest and a creamy clip for teleportation.
-Save in Geffen.
-Fire bullets in storage.
-Autoloot on.
-some specific hotkeys setup
With such a setup, the bot generates 2m zeny\hour stable in Royal Jellys. I've been using this bot for more than 2000 hours, considering multiple instances setup.

The bot does the following: navigate to Peach Tree dungeon via Warper; tp and kill Peach Trees; track hp, location, ammo, weight; refill hp\ammo from kafra and unload loot when needed; set off sound alarm when a character is not within allowed location, for example when a game administrator puts the bot into jail.

-screen.py and mouse.py contain ctypes-based input and screen-reading methods.
-client.py contains a basic task management logic, which (despite its simplicity and uglyness) was fun to develop, since I had no such experience prior to this project. I did not use any kind of guidance while writing this. Pure monkey-coding.
-run_bot.py contains UI-code. 
-features folder contains data for image-recognition. (utilizing simple cv2.match method)

This bot has not been tested for a while so I do not recommend using it. 
