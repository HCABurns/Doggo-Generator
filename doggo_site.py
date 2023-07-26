from flask import Flask, jsonify, request, render_template
from random import randint

app = Flask(__name__)

incomes = [
    { 'description': 'salary', 'amount': 5000 }
]

phrases = ["Yo", "Welcome", "This is a website","I am a cat", "I am a greek god",
           "You can not stop the spongebob", "Anchovies Mr. Squidward... Anchovies"]


doggos = [{"img":"doggo1.png","name":"Billy","breed":"Golden Retriever","fact":"Billy likes to sit on the grass and take in the sun with a smile!"},
          {"img":"doggo2.png","name":"Ollie (goodboyollie)","breed":"Chocolate Labrador","fact":"Ollie is a famous doggo with 6.7 Million TikTok followers!"}]


@app.route('/')
def landing_page():
    #phrase = phrases[randint(0,len(phrases)-1)]
    dog_number = randint(0,len(doggos)-1)
    print(dog_number)
    return render_template("index.html",random_phrase = doggos[dog_number]["name"], dog_image = doggos[dog_number]["img"])
  

@app.route('/doggos')
def get_doggos():
    return jsonify(doggos)
                   

@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204
