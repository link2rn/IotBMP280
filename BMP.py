#Librray to get data From Senser
from Adafruit_BME280 import *
import datetime
from time import sleep
import geocoder
g= geocoder.ip('me')

#Librray for Azure IoT Hub
from base64 import b64encode, b64decode
from hashlib import sha256
from urllib import quote_plus, urlencode
from hmac import HMAC
import requests
import json
import os
import time

# Azure IoT Hub
URI='sochwarestation.azure-devices.net'
KEY='2kT5rApjq3c7LQr/Tq35Of29gtp7/ddpIlgYfvkErEs='
IOT_DEVICE_ID = 'sochware_station001'
POLICY = 'iothubowner'

def generate_sas_token():
    expiry=3600
    ttl = time.time() + expiry
    sign_key = "%s\n%d" % ((quote_plus(URI)), int(ttl))
    signature = b64encode(HMAC(b64decode(KEY), sign_key, sha256).digest())

    rawtoken = {
        'sr' :  URI,
        'sig': signature,
        'se' : str(int(ttl))
    }

    rawtoken['skn'] = POLICY

    return 'SharedAccessSignature ' + urlencode(rawtoken)

def send_message(token, message):
    url = 'https://{0}/devices/{1}/messages/events?api-version=2016-11-14'.format(URI, IOT_DEVICE_ID)
    headers = {
        "Content-Type": "application/json",
        "Authorization": token    }
    data = json.dumps(message)
    print data
    response = requests.post(url, data=data, headers=headers)
    
def getData():
    now = datetime.datetime.now()
    date=now.strftime("%Y/%m/%d")
    time=now.strftime("%H:%M:%S")
    fulldate=str(now)
    sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
    degrees = sensor.read_temperature()
    pascals = sensor.read_pressure()
    hectopascals = pascals / 100
    data={
        'city':str(g.city),
        'country':str(g.state),
        'date':date,
        'time':time,
        'fulldate':fulldate,
        'temperature':degrees,
        'pressure':hectopascals      
        }
    return data
if __name__ == '__main__':

    # 1. Generate SAS Token
    token = generate_sas_token()

    #2. Sending data to IOT HUB
    while True:
        data=getData()
        send_message(token, data)
        time.sleep(1)
#while True:
 #   data=getData()
  #  sleep(1)
   # for key,val in data.items():
    #    print(key,"=>",val)
    #print("================")
    #print(getData())
#print ('Temp      = {0:0.3f} deg C'.format(degrees))
#print ('Pressure  = {0:0.2f} hPa'.format(hectopascals))
#print ('Humidity  = {0:0.2f} %'.format(humidity))
