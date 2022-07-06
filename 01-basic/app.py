import pymongo
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

# create a mongo client
client = pymongo.MongoClient( os.environ.get('MONGO_URI'),
                              ssl_cert_reqs=ssl.CERT_NONE) # create an instance of MongoClient from the pymongo package 
                                                           # and store it in the `client` variable

# retrive a database
db = client["sample_airbnb"]

listings = db.listingsAndReviews.find({
    "beds": {
        "$gte": 3
    }, 
}, {
    "name": 1,
    "beds": 1
}).limit(10)

print(listings)
for l in listings:
    print(l)