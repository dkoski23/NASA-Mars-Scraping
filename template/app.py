from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")

def index():
    return "hello"

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_test = mission_to_mars.scrape()
    print(mars_test)
    return "scrape connects"

if __name__ == "__main__":
    app.run