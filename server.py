import flask
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

import random
import math
# Mongo database
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

# Date handling
import arrow # Replacement for datetime, based on moment.js
#import datetime # But we still need time
#from dateutil import tz  # For interpreting local times

###
# Globals
###
app = flask.Flask(__name__)
import CONFIG


import uuid
app.secret_key = str(uuid.uuid4())
app.debug = CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)

import twitter
api = twitter.Api(consumer_key=CONFIG.consumer_key,
    consumer_secret=CONFIG.consumer_secret,
    access_token_key=CONFIG.access_token,
    access_token_secret=CONFIG.access_token_secret)



try:
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.service
    collectionTwits = db.twits
except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    #sys.exit(1)

#############
####Pages####
#############


### Home Page ###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('page_not_found.html'), 404

################
###functions###
################

@app.route("/_getHashtagData")
def preData():
    aReturn = request.args.get('aThing',0,type=str)
    aVal = json.loads(aReturn)
    hashtag = aVal.get("hashtag")
    print(hashtag)
    d = {"result":"true", "val":hashtag}
    users = api.GetUserTimeline("CNN")
    print([u.screen_name for u in users])
    return jsonify(d)

if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,threaded=True)
