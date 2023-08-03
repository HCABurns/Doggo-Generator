from flask import Flask, jsonify, request, render_template
from random import randint
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import base64

app = Flask(__name__)

uri = "mongodb+srv://admin:lE8686QBDMQFtM5S@dog-generator.g9bskdd.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


@app.route('/')
def landing_page():
    #dog_number = randint(0,len(doggos)-1)
    #print(dog_number)

    #Upload the images to the database.
    """
    for i in range(len(doggos)):
        with open(f"static/{doggos[i]['img']}", "rb") as imageFile:
            b64 = base64.b64encode(imageFile.read())
        #im.save(image_bytes, format='JPEG')
            
        client.dogs.dog.insert_one({"img":b64,"name":doggos[i]["name"],"breed":doggos[i]["breed"],"fact":doggos[i]["fact"]})

    for x in client.dogs.dog.find():
        image64 = x["img"].decode()
        #print(image64)
    """
    
    #Get random record
    pipeline = [{'$sample': {'size': 1}}]
    
    #db.dogs.dog.aggregate([{ $sample: { size: 1 } }])
    for res in client.dogs.dog.aggregate(pipeline):
        dog_image = res["img"].decode()
        dog_name = res["name"]
        dog_breed = res["breed"]
        dog_Fact = res["fact"]
    
    return render_template("index.html",doggo_name = dog_name,
                                        dog_image = dog_image,
                                        doggo_breed = dog_breed,
                                        doggo_fact = dog_Fact)


@app.route('/doggos', methods = ['GET'])
def get_doggos():
    """
    This function will return all the dogs in the list.
    """
    out = []
    for dog in client.dogs.dog.find():
        dog = convert_data(dog)
        out.append(dog)
    return jsonify(out)
                   

@app.route('/doggo/<int:doggo_id>', methods = ['GET'])
def get_doggo(doggo_id):
    """
    This function will return a single JSON Object correlating to a single dog.

    Parameters
    --------------------
    int : doggo_id
        This is the ID for the dog.
    """
    for i,dog in enumerate(client.dogs.dog.find()):
        if i == doggo_id:
            return jsonify(convert_data(dog)) 
    return render_template("error.html"), 404


@app.route('/breed/<string:doggo_breed>', methods = ['GET'])
def get_doggo_breed(doggo_breed):
    """
    This function will return all JSON Objects correlating to a single dog breed.

    Parameters
    --------------------
    str : doggo_breed
        This is the breed of the dog to be returned.
    """
    dogs = []
    for dog in client.dogs.dog.find():
        dog = convert_data(dog)
        if dog["breed"].lower() == doggo_breed.lower():
            dogs.append(dog)
    return jsonify(dogs)


@app.route('/add', methods = ['GET','POST'])
def add_doggo():
    """
    This function will return all the dogs in the list.
    """
    if request.method == 'GET':
        return render_template("add.html")
    if request.method == 'POST':
        name = request.form.get("name")
        fact = request.form.get("fact")
        breed =request.form.get("breed")
        image = request.files['file']
        b64 = base64.b64encode(image.read())

        client.dogs.dog.insert_one({"img":b64,"name":name,"breed":breed,"fact":fact})

        
        #print(base64.b64encode(file))
        return render_template("add.html") , 201


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 500 status explicitly
    return render_template('error.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 500 status explicitly
    return render_template('server_error.html'), 500


def convert_data(record):
    """
    This will convert a record from the database to a useable state.

    Parameters
    -------------------
    record : Dict
        This is a dictionary of a document retrieved from the MongoDB database.

    Return
    -------------------
    dict : A dictionary without the id and the image is decoded from base64. 
    """
    record.pop("_id")
    tmp = record["img"]
    record["img"] = tmp.decode()
    return record
    
"""
@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204
"""
