from flask import Flask, render_template, request
import pymongo
import ssl
import os
from dotenv import load_dotenv


load_dotenv()

# create a connection to the Mongo database
client = pymongo.MongoClient(os.environ.get('MONGO_URI'),
                             ssl_cert_reqs=ssl.CERT_NONE)

db = client["sample_airbnb"]
# end connecting to database

app = Flask(__name__)
app.secret_key=os.environ.get('SECRET_KEY')

@app.route('/')
def index():
    # get the first ten listings and display them
    listings = db.listingsAndReviews.find({}).limit(10)   
    return render_template('listing.html', listings=listings)

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)