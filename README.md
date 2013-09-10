Wallpaper Dump Script
===================

A python script/osx application to pull albums from reddit.com/r/wallpaperdump and set them to be your desktop wallpaper

# Installation

A requirements.txt file is included and will install any requirements using the command

`pip install -r requirements.txt`

# Running it

There are three ways to use this/these scripts:

	1. `python app.py` - will run app.py as expected in the terminal
	2. `./compile_and_run.sh` - will compile app.py into an OSX .app file and then run it in the terminal. The .app file can be run separately not in a terminal later.
	3. `python wallpaper_download.py` - this will download a single album and then exit. No automatic cycling will occur and no osx status bar application will run.
