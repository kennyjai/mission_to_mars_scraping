from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# drops collection if availble to remove dupes
mongo.db.collection.drop()

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():

	# Find data
    mars_data = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

	# Run scraped functions
    data = scrape_mars.scrape()

    # Store results into a dictionary
    mars_data = {
        "news_title": data["news_title"],
        "news_p": data["news_p"],
        "featured_img_url": data["featured_img_url"],
        "mars_weather": data["mars_weather"],
        "html_table": data["html_table"],
        "hemisphere_image_urls": data["hemisphere_image_urls"],
    }

    # Insert forecast into database
    mongo.db.collection.insert_one(mars_data)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
