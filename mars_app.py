from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# # setup Flask
app = Flask(__name__)

# set up Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# # Flask routes
@app.route("/")
def home():
   mars_info = mongo.db.mars_info.find()
   return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scrape():
    mars_info = mongo.db.mars_info
    mars_info_data = scrape_mars.mars_scrapes()
    mars_info.update({}, mars_info_data, upsert=True)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
