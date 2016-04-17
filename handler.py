#!/usr/bin/python3

# This code goes into the docker image.

def handle(request):
  return globals()[request['function_name']]()

def sayHello():
  return {'response': 'Hello Chariot!'}
