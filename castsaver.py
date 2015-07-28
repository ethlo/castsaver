#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import time
import pychromecast
import random
from random import randint
import logging
import ConfigParser

class CastSaver:

	# Constants
	BACKDROP_APP_ID = 'E8C28D3C'
	DEFAULT_MEDIAPLAYER_APP_ID = 'CC1AD845'
	
	def __init__(self):
		# Time for last idle application
		self.idle = 0

		# Load configuration from file
		self.config = ConfigParser.ConfigParser()
		self.config.read('castsaver.ini')
		self.check_interval = self.config.getint('settings', 'poll_interval')
		self.display_interval = self.config.getint('settings', 'display_time')
		self.max_idle_interval = self.config.getint('settings','max_idle')
		self.mediaSource = self.config.get('settings', 'media_source')
		self.run_if_backdrop_mode = self.config.getboolean('settings', 'run_if_backdrop_mode')
		self.logFile = self.config.get('logging', 'log_file')
		self.logLevel = self.config.get('logging', 'log_level')
		self.available_for_status = self.config.get('settings', 'available_for_status').split(',')
		self.available_for_status.append(CastSaver.DEFAULT_MEDIAPLAYER_APP_ID)

		# Setup logging
		self.logger = logging.getLogger(__name__)
		if not self.logFile:
                        handler = logging.StreamHandler(sys.stdout)
		else:
			handler = logging.FileHandler(self.logFile)
		self.logger.setLevel(logging.getLevelName(self.logLevel))
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)

		# pyChromecast logger
                logging.getLogger('pychromecast.socket_client').addHandler(handler);

		# Discover chromecasts
		self.chromeCasts = pychromecast.get_chromecasts_as_dict()
		if len(self.chromeCasts) == 0:
			self.logger.info('Discovered no chrome cast devices. Exiting')
			sys.exit()
		self.logger.info('Dicovered chromecast devices: ' + str(self.chromeCasts.keys()))

		while True:
			for name, cast in self.chromeCasts.iteritems():
 				self.check(cast)
  			
			# Wait until next check
			self.logger.debug('Waiting to poll again:' + str(self.check_interval))
			time.sleep(self.check_interval)

	def startScreenSaver(self, cast):
		mc = cast.media_controller
		
		if self.mediaSource and os.path.isfile(self.mediaSource) and os.path.getsize(self.mediaSource) > 0:
			lines = open(self.mediaSource).read().splitlines()
			url = random.choice(lines)
		else:
			url = 'http://wallpaperfx.com/view_image/a-1920x1080-wallpaper-' + str(randint(100,16000)) + '.jpg'		

		self.logger.debug('Displaying ' + url)
		type = '';
		mc.play_media(url, type);

		# Display media for defined period
                time.sleep(self.display_interval)

	def check(self, cast):
		self.logger.debug('Checking status of ' + str(cast))
		
		status = cast.status
		
		if status:
			appId = status.app_id
			appName = status.display_name

			if appId == CastSaver.BACKDROP_APP_ID and self.run_if_backdrop_mode:
				self.logger.info('Backdrop app running, starting screensaver');
				self.startScreenSaver(cast)
			elif appId == CastSaver.DEFAULT_MEDIAPLAYER_APP_ID:
				mc = cast.media_controller
                                if mc.status.player_is_idle:
                                	self.startScreenSaver(cast)
			elif appId in self.available_for_status:
				mc = cast.media_controller
				self.logger.debug('Media status for ' + appId + ' - ' + appName + ': ' + mc.status.player_state);
				if (mc.status.player_is_idle or mc.status.player_is_paused):
					if self.idle == 0:
						self.idle = time.time()
						self.logger.info('Discovered idle/paused application ' + appName)
				else:
					if self.idle != 0:
						self.logger.info('Discovered active application ' + appName + ', resetting idle timer')
						self.idle = 0

				if self.idle > 0 and (time.time() > self.idle + self.max_idle_interval):
					self.logger.info('Application ' + appName + ' has been idle too long, starting screensaver')
					self.startScreenSaver(cast);
			else:
				self.logger.info('Unsupported application running: ' + appId + " - " + appName)
		else:
			self.logger.info('No status available')
try:
	print('CastSaver - Chromecast screen-saver');
	CastSaver();	
except KeyboardInterrupt:
	print('Exiting by request')
