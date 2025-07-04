from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["talentshow"]
waitlist = db["participants"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.form)
        name = request.form["name"]
        age = request.form["age"]
        talent = request.form["talent"]
        image_url = request.form.get("image_url")

        if name and age and talent and image_url:
            waitlist.insert_one({
                "name": name,
                "age": age,
                "talent": talent,
                "image": image_url
            })
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/fisayo")
def admin():
    participants = list(waitlist.find())
    return render_template("admin.html", participants=participants)

if __name__ == "__main__":
    app.run(debug=True)