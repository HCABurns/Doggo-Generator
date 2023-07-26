from flask import Flask, jsonify, request, render_template
from random import randint

app = Flask(__name__)

incomes = [
    { 'description': 'salary', 'amount': 5000 }
]

phrases = ["Yo", "Welcome", "This is a website","I am a cat", "I am a greek god",
           "You can not stop the spongebob", "Anchovies Mr. Squidward... Anchovies"]


doggos = [{"img":"doggo1.png","name":"Billy","breed":"Golden Retriever","fact":"Billy likes to sit on the grass and take in the sun with a smile!"},
          {"img":"doggo2.png","name":"Ollie (@goodboyollie)","breed":"Chocolate Labrador","fact":"Ollie is a famous doggo with 6.7 Million TikTok followers!"}]


@app.route('/')
def landing_page():
    #phrase = phrases[randint(0,len(phrases)-1)]
    dog_number = randint(0,len(doggos)-1)
    print(dog_number)
    return render_template("index.html",doggo_name = doggos[dog_number]["name"],
                                       dog_image = doggos[dog_number]["img"],
                                       doggo_breed = doggos[dog_number]["breed"],
                                       doggo_fact = doggos[dog_number]["fact"])

@app.route('/doggos')
def get_doggos():
    return jsonify(doggos)
                   

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
        return "<b>Error! This ID does not correlate to a valid doggo!</b>"
    return jsonify(doggos[doggo_id])


@app.route('/breed/<string:doggo_breed>', methods = ['GET'])
def get_doggo_breed(doggo_breed):
    """
    This function will return all JSON Objects correlating to a single dog breed.

    Parameters
    --------------------
    int : doggo_breed
        This is the breed of the dog to be returned.
    """
    dogs = []
    for dog in doggos:
        if dog["breed"] == doggo_breed:
            dogs.append(dog)
    return jsonify(dogs)
    #return "<b>Error! This ID does not correlate to a valid doggo!</b>"
    #return jsonify(doggos[doggo_id])

"""
@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204
"""
