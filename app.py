#!/usr/bin/env python

#Mac objc shit
import objc, re, os
from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder, AppHelper

from appscript import app as appscript_app, its

from wallpaper_download import WallpaperDownloader

class Timer(NSObject):
	
	statusbar = None

	def init(self):

		self = super(Timer, self).init()
		if self is None: return None

		self.downloader = WallpaperDownloader()
		return self

	def applicationDidFinishLaunching_(self, notification):
		
		statusbar = NSStatusBar.systemStatusBar()
		# Create the statusbar item
		self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength).retain()
		
		# Set initial image
		self.statusitem.setImage_(NSImage.alloc().initByReferencingFile_('redit-alien-small.png'))
		
		#self.statusitem.setTitle_('Wall')
		# Let it highlight upon clicking
		self.statusitem.setHighlightMode_(1) 
		# Set a tooltip
		self.statusitem.setToolTip_('Sync Trigger')

		# Build a very simple menu
		self.menu = NSMenu.alloc().init()
	
		# Sync event is bound to sync_ method
		menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Sync...', 'sync:', '')
		self.menu.addItem_(menuitem)
	
		# Default event
		menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
		self.menu.addItem_(menuitem)
	
		# Bind it to the status item
		self.statusitem.setMenu_(self.menu)

		# Get the timer going
		self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(NSDate.date(), 60.0, self, 'tick:', None, True)
		NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
		self.timer.fire()

	def sync_(self, notification):
		self.downloader.download_album()

	def tick_(self, notification):
		#change to next image
		appscript_app("System Events").desktops[its.display_name == u"Color LCD"].picture.set("/Users/michaellittle/Desktop/imgres.jpeg")


if __name__ == "__main__":
	app = NSApplication.sharedApplication()
	delegate = Timer.alloc().init()
	app.setDelegate_(delegate)
	AppHelper.runEventLoop()