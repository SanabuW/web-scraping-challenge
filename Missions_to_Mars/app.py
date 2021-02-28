# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import libraries
from bs4 import BeautifulSoup as bs
import requests
import time
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape_nasa


# %%
# set up Flask
app = Flask(__name__)
# setup MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_db"
mongo = PyMongo(app)

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Select database and collection to use
db = client.scrape_db
mars_coll = db.mars_coll

# %%
@app.route("/")
def index():

    search_result = mars_coll.find_one()
    return render_template("index.html", search_result=search_result)

# %%
@app.route("/scrape")
def scrape():
    # Move to collection
    collection = mars_coll
    # perform scrape and save result
    scrape_result = scrape_nasa()
    collection.update({}, scrape_result, upsert=True)
    # # Insert scrape dictionary into collection
    # collection.insert_one(scrape_result)
    return redirect("/", code=302)

client.close()

if __name__ == "__main__":
    app.run(debug=True)


