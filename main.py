#coding: utf-8

import time
# import numpy as np
from datetime import datetime
from my_bme import *
from gps import *
import threading

trial_until_saving = 20
data_type_num = 5
interval_second = 30
SAVE = False

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
      # x = []
      # all_data = np.array(x)

      for i in range(trial_until_saving):
        latitude = gpsd.fix.latitude
        longitude = gpsd.fix.longitude
        gps_time = gpsd.utc
        height = gpsd.fix.altitude
        pressure,temperature,humidity = readData()
        print gps_time, lati, long, height, pressure, temperature, humidity

        # if get gps data update data
        if latitude != 'nan' and longitude != 'nan' and height != 'nan':
            temp_data = [latitude,longitude,height,pressure,temperature,humidity]
        time.sleep(interval_second)
      if SAVE==True:
        print '*'*10 + ' saving file ' +'*'*10
        fd = open('log.csv','a')
        fd.write(temp_data)
        fd.close()
        # all_data = np.resize(all_data,(data_num, data_type))
        # np.savetxt('data/'+first_time+'.csv',all_data,delimiter=",")
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp_running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."
