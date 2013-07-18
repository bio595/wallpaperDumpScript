from distutils.core import setup
import py2app

setup(
	name="Wallpaper Dump",
	app=['app.py'],
	data_files=['reddit-alien-small.png', 'reddit-alien-syncing.png'])