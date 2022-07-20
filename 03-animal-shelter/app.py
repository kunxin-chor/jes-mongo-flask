from flask import Flask, render_template, request, url_for, redirect
import os
from dotenv import load_dotenv
import certifi
import pymongo

# import in ObjectId function
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = "my_animal_shelter"
client = pymongo.MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[DB_NAME]

@app.route('/')
def index():
    return "Hello world"

@app.route('/animals')
def show_all_animals():
    animals = db.animals.find({})
    return render_template('all_animals.html', animals=animals )

@app.route('/animals/create')
def create_animal():
    return render_template('create_animal_form.html')

@app.route('/animals/create', methods=["POST"])
def process_create_animal():
    """
     db.animals.insertOne({
         animal_name: "Biscuit",
         age: 3,
         species: "Dog",
         breed: "Golden Retriever"
     })
    """
    db.animals.insert_one({
        "animal_name": request.form.get('animal_name'),
        "age": int(request.form.get('age')),
        "species": request.form.get('species'),
        "breed": request.form.get('breed')
    })
    return "animal added"

@app.route('/animals/<animal_id>/update')
def update_animal(animal_id):
    animal = db.animals.find_one({
        '_id': ObjectId(animal_id)
    })
    return render_template('update_animal_form.html', animal=animal)

@app.route('/animals/<animal_id>/update', methods=["POST"])
def process_update_animal(animal_id):
    db.animals.update_one({
        '_id':ObjectId(animal_id)
    },{
        "$set": {
        "animal_name": request.form.get('animal_name'),
        "age": int(request.form.get('age')),
        "species": request.form.get('species'),
        "breed": request.form.get('breed')
        }
    })
    return redirect(url_for('show_all_animals'))

# if this file is being ran as main
if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)