import requests
import json


#Get the outcome of the salary

#First send a request to the url and get returned the information
#on that specific URL.
response = requests.get(url = "http://127.0.0.1:5000/incomes")

#Returned is a response object and the text can be extracted from it.
print(type(response))
print(response.text)

#Now it can be converted back into a json object for processing.
resp = json.loads(response.text)
print(resp[0]["description"])
