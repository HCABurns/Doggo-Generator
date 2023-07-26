import requests
import json


#Put the new salary into the "database" using the API and PUT

#First create a new json object that is to be added.
new_record = {"description":"salary","amount":300}
             
#Now call the URL with a PUT operation with the new record.
response = requests.post(url = "http://127.0.0.1:5000/incomes", json = new_record)

#Print the output
print(response.text)
