#!/usr/bin/python3

from chariot import *

client = PrashtiClient()

request = {
    'device_id' : 'test1',
    'request_id' : randomReqId(),
    'function_name' : 'testFunc',
    'arguments' : [],
    'extra_data' : {}
}

installRequest = {
    'device_id' : 'device42',
    'request_id' : randomReqId(),
    'function_name' : 'chariotDeviceSetup',
    'arguments' : [],
    'extra_data' : {'dockerImage': '2020saurav/chariot-hello:1.0'}
}

helloRequest = {
    'device_id' : 'device42',
    'request_id' : randomReqId(),
    'function_name' : 'sayHello',
    'arguments' : [],
    'extra_data' : {}
}

response = client.call(helloRequest)
print(response)
