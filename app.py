from flask import Flask, render_template, request
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    # App Instance
    app = Flask(__name__)
    # Db Instance
    client = MongoClient(os.getenv('MONGODB_URI'))
    app.db = client.remainderist

    @app.route('/', methods=["POST", "GET"])
    def home():
        if request.method == "POST":
            eventTitle = request.form.get('eventTitle')
            eventDescription = request.form.get('eventDescription')
            eventTime = request.form.get('eventTime')
            eventTime = datetime.fromisoformat(eventTime)
            eventTime = eventTime.strftime('%d %b %y @ %I:%M%p')
            app.db.events.insert_one({"Title" : eventTitle, "Description" : eventDescription, "Time" : eventTime})
        # Retrieve from DB
        events = [ (event['Title'], event['Description'], event['Time']) for event in app.db.events.find({}) ]
        return render_template('home.html', events=events)

    return app