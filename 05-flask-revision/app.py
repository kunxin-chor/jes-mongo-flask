from datetime import datetime
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
DB_NAME = "sample_analytics"
# tlsCAFile is for enabling access to mongoDB from localhost
client = pymongo.MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[DB_NAME]

@app.route('/customers')
def show_all_customers():
    # route to display the all customers
    customers = db.customers.find()
    return render_template('customers.html', customers=customers)

@app.route('/customers/<customer_id>/update')
def update_customer(customer_id):
    # find the customer that we want to update
    customer = db.customers.find_one({
        '_id': ObjectId(customer_id) 
    })

    # send the customer to the update form
    return render_template('update_customer_form.html', customer=customer)

@app.route('/customers/<customer_id>/update', methods=['POST'])
def process_update_customer(customer_id):
    # find the customer that we want to update
    customer = db.customers.find_one({
        '_id': ObjectId(customer_id) 
    })

    # update the customer
    customer['name'] = request.form['name']
    customer['username'] = request.form['username']
    customer['email'] = request.form['email']
    customer['address'] = request.form['address']
    customer['birthdate'] = datetime.strptime(request.form['birthdate'], "%Y-%m-%d")

    # update the customer in the database
    db.customers.update_one(
        {'_id': ObjectId(customer_id)},
        {'$set': customer}
    )

    # redirect to the customer's page    
    return redirect(url_for('show_all_customers', customer_id=customer_id))
    

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)
