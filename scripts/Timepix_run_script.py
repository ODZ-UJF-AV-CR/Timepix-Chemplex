import os
import time
import numpy as np

dic = {"MiniPIX H08-W0276":3, "MiniPIX I08-W0276":4}
dic_config = {"MiniPIX H08-W0276":"/home/user/Documents/Experiments/Radiotherapy_cells/MiniPIX-H08-W0276.xml",
              "MiniPIX I08-W0276":"/home/user/Documents/Experiments/Radiotherapy_cells/MiniPIX-I08-W0276.xml"}

acqCount = 150 # number of frames 
acqTime = 0.1 # seconds
fileType = 1 # auto detect, 0 = no output file
biasVoltage = 80
sleep_time = 300 # seconds
path = "/home/user/Documents/Experiments/Radiotherapy_cells/Lu177_cells"
path_config = "/home/user/Documents/Experiments/Radiotherapy_cells"

def usb_switch(cond=True, ports=[3, 4]):
    for i in ports:
        if cond:
            string = "uhubctl -a on -p " + str(i)
        else:
            string = "uhubctl -a off -p " + str(i)
        os.system(string)
        time.sleep(1)

usb_switch(True, dic.values())

alldevices = pixet.devices() # get all devices (including motors)
detectors = pixet.devicesByType(1) # get all connected Medipix/Timepix devices

usb_switch(False, dic.values())

for i in range(0, 2400):
    usb_switch(True, dic.values())
    detectors[0].reconnect()

    alldevices = pixet.devices() # get all devices (including motors)
    detectors = pixet.devicesByType(1) # get all connected Medipix/Timepix devices
        
    for detector in detectors:
        detector.loadConfigFromFile(dic_config[detector.fullName()])
        bias_str = detector.setBias(biasVoltage)
        outputFile = os.path.join(path, detector.fullName() + "_" + str(i) + ".clog")
        detector.doSimpleAcquisition(acqCount, acqTime, fileType, outputFile)
            
    usb_switch(False, dic.values())   
    
    time.sleep(sleep_time)
    print("ende")
 
usb_switch(False, dic.values())
