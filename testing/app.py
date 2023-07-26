from flask import Flask, jsonify, request
from random import randint

app = Flask(__name__)

incomes = [
    { 'description': 'salary', 'amount': 5000 }
]

phrases = ["Yo", "Welcome", "This is a website","I am a cat"]


@app.route('/')
def landing_page():
    return f"<h1>{phrases[randint(0,len(phrases)-1)]}</h1>"
  


@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204
