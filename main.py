#coding: utf-8

import time
# import numpy as np
from datetime import datetime
from my_bme import *
from gps import *
import threading
import math

# for test
trial_until_saving = 3
interval_second = 3
SAVE = True

# for real use
# trial_until_saving = 20
# interval_second = 30
# SAVE = True

gpsd = None #seting the global variable
gpsp_running = True
 
#os.system('clear') #clear the terminal (optional)

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    gpsp_running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp_running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:

      for i in range(trial_until_saving):
        latitude = gpsd.fix.latitude
        longitude = gpsd.fix.longitude
        gps_time = gpsd.utc
        height = gpsd.fix.altitude
        pressure,temperature,humidity = readData()
        print gps_time[0:10],gps_time[11:19], latitude, longitude, height, pressure, temperature, humidity

        if not (math.isnan(latitude) or math.isnan(longitude) or math.isnan(height)):
            temp_data = [gps_time[0:10],gps_time[11:19],latitude,longitude,height,pressure,temperature,humidity]
        time.sleep(interval_second)
      try:
        temp_data
      except NameError:
        print 'No data to save!'
        continue

      if SAVE==True:
        print '*'*10 + 'saving file' + '*'*10
        fd = open('data/log.csv','a')
        writer = csv.writer(fd)
        writer.writerow(temp_data)
        fd.close()
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp_running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."
