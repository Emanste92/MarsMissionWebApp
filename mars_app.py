from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# # setup Flask
app = Flask(__name__)


# work on setting up mongodb connection
# work on aligning whats in the index.html to line up properly

# set up Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")



# # Flask routes
@app.route("/")
def home():
   mars_info = mongo.db.collection.find_one()
   return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scrape():
    mars_info = scrape_mars.mars_scrapes()

    mongo.db.collection.update({}, mars_info, upsert=True)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
