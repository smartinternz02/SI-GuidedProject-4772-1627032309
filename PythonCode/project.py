import wiotp.sdk.device
import time
import random
import requests

myConfig = { 
    "identity": {
        "orgId": "1zlsjs",
        "typeId": "VITshre",
        "deviceId":"700425"
    },
    "auth": {
        "token": "7004251110"
    }
}


def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    m=cmd.data['command']
    
    if(m == "pumpon"):
        print("....PUMP is ON....")
    elif(m == "pumpoff"):
        print("....PUMP is OFF....")
    elif(m == "feedon"):
        print("....FEED is ON....")
        alertf=requests.get('https://www.fast2sms.com/dev/bulkV2?authorization=zq4NkwlYHGE7Is5yXgb96PU1naWBQoicjeMRvAx8rpu03OKSJTTpDG7Y8MfHR5ImsF02bZBAJdul1Q6o&route=q&message=Alert:%20The%20feeding%20process%20has%20been%20ACTIVATED&language=english&flash=0&numbers=7004251110')
        print(alertf.text)
    elif(m == "feedoff"):
        print("....FEED is OFF....")
    else:
        print(f"Feeding Motor speed is set to {m}")
             
    print()

    

client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

c=0

while True:
##    waterlevel=random.randint(0,100)
    waterlevel=65
    if(waterlevel <= 60 and c!=1):
        c=1
        alert=requests.get('https://www.fast2sms.com/dev/bulkV2?authorization=zq4NkwlYHGE7Is5yXgb96PU1naWBQoicjeMRvAx8rpu03OKSJTTpDG7Y8MfHR5ImsF02bZBAJdul1Q6o&route=q&message=Alert:%20Water%20Level%20Low&language=english&flash=0&numbers=7004251110')
        print(alert.text)
        
    myData={'waterlevel':waterlevel}
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: %s", myData)
    client.commandCallback = myCommandCallback
    time.sleep(2)
client.disconnect()

