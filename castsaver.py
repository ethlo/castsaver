#!/usr/bin/env python
from __future__ import print_function
import time
import pychromecast
import random
import logging

class CastSaver:

	# Constants
	BACKDROP_APP_ID = 'E8C28D3C'
	DEFAULT_MEDIAPLAYER_APP_ID = 'CC1AD845'
	
	# Available to be queried for media status
	AVAILABLE_FOR_STATUS = {
		'CC1AD845': 'Default media player',
		'DAEE0AA4': 'TV 2 Sumo', 
		'3AEDF8D1': 'NRK TV'
	}
	
	# Configuration
	logFile = 'castsaver.log'
	logLevel = logging.INFO
	check_interval = 5;
	display_interval = 30;
	max_idle_interval = 60;

	def __init__(self):
		# Time for last idle application
		self.idle = 0

		# Setup logging
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.INFO)
		handler = logging.FileHandler(self.logFile)
		handler.setLevel(self.logLevel)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)

		self.chromeCasts = pychromecast.get_chromecasts_as_dict()
		self.logger.info('Dicovered chromecast devices: ' + str(self.chromeCasts.keys()))

		while True:
			for name, cast in self.chromeCasts.iteritems():
 				self.check(cast)
  			
			# Wait until next check
			time.sleep(CastSaver.check_interval)

	def startScreenSaver(self, cast):
		mc = cast.media_controller
		
		lines = open('media.txt').read().splitlines()
		url = random.choice(lines)
		self.logger.debug('Displaying ' + url)
		type = '';
		mc.play_media(url, type);

		# Display media for defined period
                time.sleep(CastSaver.display_interval)

	def check(self, cast):
		status = cast.status
		
		if status:
			appId = status.app_id
			appName = status.display_name

			if appId == CastSaver.BACKDROP_APP_ID:
				self.logger.info('Backdrop app running, starting screensaver');
				self.startScreenSaver(cast)
			elif appId == CastSaver.DEFAULT_MEDIAPLAYER_APP_ID:
				mc = cast.media_controller
                                if mc.status.player_is_idle:
                                	self.startScreenSaver(cast)
			elif appId in CastSaver.AVAILABLE_FOR_STATUS:
				mc = cast.media_controller
				self.logger.debug('Media status for ' + appId + ' - ' + appName + ': ' + mc.status.player_state);
				if (mc.status.player_is_idle or mc.status.player_is_paused):
					if self.idle == 0:
						self.idle = time.time()
						self.logger.info('Discovered idle/paused player ' + str(self.idle))
				else:
					if self.idle != 0:
						self.logger.info('Discovered active player, resetting idle timer')
						self.idle = 0

				if self.idle > 0 and (time.time() > self.idle + self.max_idle_interval):
					self.logger.info('Current application has been idle too long, starting screensaver')
					self.startScreenSaver(cast);
			else:
				self.logger.debug('Unsupported application running: ' + appId + " - " + appName)

try:
	print('CastSaver - Chromecast screen-saver');
	CastSaver();	
except KeyboardInterrupt:
	print('Exiting by request')
