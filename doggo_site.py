from flask import Flask, jsonify, request, render_template, flash
from random import randint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from bson.errors import InvalidId
import dbInfo 
import base64

app = Flask(__name__)
app.config['MAX_CONTENT_PATH'] = 16 * 1000000 #16MB limit (For MongoDB)
app.secret_key = dbInfo.get_secret_key()

uri = "mongodb+srv://{}:{}@dog-generator.g9bskdd.mongodb.net/?retryWrites=true&w=majority&appName=dog-generator".format(dbInfo.get_username(),dbInfo.get_password())
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    print("Attempting Ping...")
    client.admin.command('ping')
    print("Pinged deployment. Successfully connected to MongoDB!")
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
    out = []
    for dog in client.dogs.dog.find():
        dog = convert_data(dog)
        out.append(dog)
    return jsonify({
        "doggos": out,
        "count": len(out)
    })
                   
"""
@app.route('/doggo/<int:doggo_id>', methods = ['GET'])
def get_doggo(doggo_id):
"""
"""
    This function will return a single JSON Object correlating to a single dog.

    Parameters
    --------------------
    int : doggo_id
        This is the ID for the dog.
"""
"""
    for i,dog in enumerate(client.dogs.dog.find()):
        if i == doggo_id:
            return jsonify(convert_data(dog)) 
    return render_template("error.html"), 404
"""
    
@app.route('/doggo/<string:doggo_id>', methods=['GET'])
def get_doggo(doggo_id):
    try:
        dog = client.dogs.dog.find_one({'_id': ObjectId(doggo_id)})
        if dog:
            return jsonify(convert_data(dog))
        else:
            return jsonify({'error': 'Dog not found'}), 404
    except:
        return jsonify({'error': 'Invalid ID'}), 400

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

        if not name or not fact or not breed or not image or ".png" not in image.filename:

            if not name:
                message = "Missing Data: Name is empty!"
            elif not breed:
                message = "Missing Data: Breed is empty!"
            elif not fact:
                message = "Missing Data: Fact is empty!"
            else:
                message = "Error: Empty or incorrect file type. Only PNG accepted!"
            
            return render_template("add.html", doggo_name = name,
                                               doggo_fact = fact,
                                               doggo_breed = breed,
                                               doggo_image = image,
                                               message = message)

        client.dogs.dog.insert_one({"img":b64,"name":name,"breed":breed,"fact":fact})
        
        #print(base64.b64encode(file))
        return render_template("add.html") , 201


@app.errorhandler(404)
def page_not_found(e):
    if request.path.startswith('/doggo') or request.path.startswith('/doggos'):
        return jsonify({'error': 'Not found'}), 404
    return render_template('error.html'), 404


@app.errorhandler(500)
def page_not_found(e):
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
    record["_id"] = str(record["_id"])
    tmp = record["img"]
    record["img"] = tmp.decode()
    return record
    
#if __name__ == "__main__":
#    app.run()    

