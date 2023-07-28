from flask import Flask, jsonify, request, render_template
from random import randint
from pymongo import MongoClient
from pymongo.server_api import ServerApi
#from PIL import Image
#from bson import Binary
#import io
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

"""
#client = MongoClient('mongodb://localhost:27017/', username='admin', password='j5P1wwZLIICqy4J0')
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.dogs
# Access collection of the database
mc=db.dog
"""

"""
doggos = [{"img":"doggo1.png","name":"Billy","breed":"Golden Retriever","fact":"Billy likes to sit on the grass and take in the sun with a smile!"},
          {"img":"doggo2.png","name":"Ollie (@good.boy.ollie)","breed":"Labrador","fact":"Ollie is a famous doggo with 6.7 Million TikTok followers!"},
          {"img":"doggo3.png","name":"Tato (@good.boy.tato)","breed":"Labrador","fact":"Tato is the brother of famous doggo @good.boy.ollie and also qualified for the 2024!"},
          {"img":"doggo4.png","name":"Barkley","breed":"Shiba Inu","fact":"Barkley loves to travel around the US with his owners!"},
          {"img":"doggo5.png","name":"Hector (@hectorthechocolabo)","breed":"Labrador","fact":"Hector is a famous instagram doggo with 132K followers!"},
          {"img":"doggo6.png","name":"Yogi","breed":"Labrador","fact":"Yogi, also known as baby Yogi, is the brother of famous instagram doggo @hectorthechocolabo."},
          {"img":"doggo7.png","name":"Dex","breed":"Rotweiler","fact":"Dex is a goofy doggo who loves nothing more than chasing a frisbee!"},
          {"img":"doggo8.png","name":"Tucker Budzyn (@TuckerBudzyn)","breed":"Golden Retriever","fact":"Tucker is the worlds most famous pet with a following of 10.4 million on TikTok. Tucker also has a staggering net worth of $2 million!"}]
"""

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
    
    
    #Get random record??????
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


@app.route('/doggos')
def get_doggos():
    """
    This function will return all the dogs in the list.
    """

    out = []
    for x in client.dogs.dog.find():
        x.pop("_id")
        tmp = x["img"]
        x.pop("img")
        x["img"] = tmp.decode()#.replace("'", '"')
        print(x)
        out.append(x)
    return jsonify(out)#jsonify(x)
                   

@app.route('/doggo/<int:doggo_id>', methods = ['GET'])
def get_doggo(doggo_id):
    """
    This function will return a single JSON Object correlating to a single dog.

    Parameters
    --------------------
    int : doggo_id
        This is the ID for the dog.
    """
    if doggo_id > len(doggos) or doggo_id < 0:
        return render_template("error.html"), 404
    return jsonify(doggos[doggo_id])


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
    for dog in doggos:
        if dog["breed"] == doggo_breed:
            dogs.append(dog)
    return jsonify(dogs)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html'), 404

"""
@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204
"""
