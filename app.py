from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():

	# Find data
    mars_data = mongo.db.mars.find_one()

    # return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():
	# Run scraped functions
    data = scrape_mars.scrape()
    mars_data = mongo.db.mars
    mars_data.update({}, data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
