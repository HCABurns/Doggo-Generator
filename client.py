import requests

# Url for local host as testing only.
url = "http://localhost:5000/"

# Hashmap for dealing with errors:
errors = {404:"Error Occured - Resource not found.\n",500:"Error Occured - Server error.\n"}

# Get an extension a user would use to retrieve data.
answer = " "
while  answer != "quit":
    try:
        # Get extension.
        ext = input("Enter the extension: ")

        if ext == "quit":break

        # Retrieve the data from the localhost and return as json.
        response = requests.get(url+ext)

        # Provide response if error occurs.
        if response.status_code in errors:
            print(errors[response.status_code])
            #continue

        # Get the data as a json.
        data = response.json()

        # Print basic information as a usecase for retrieving the data.
        if "doggo/" in ext:
            print(data["_id"])
            print(data["name"])
            print(data["breed"])
            print(data["fact"])

        if "doggos" in ext:
            print("Number of doggos retrieved:",data["count"])
            print("Doggo 1 Name:",data["doggos"][0]["name"])
            
    except:
        print("Error Occurred - Server is down or invalid input.\nPlease try again.\n")
