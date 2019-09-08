"""
This is the microservice-wrapper around scholarly module authored by 
Steven A. Cholewniak. Scholarly is a Google Scholar scraper. The microservice
serves mainly for getting the scholar information with plain javascript in
static websites.
"""


from flask import Flask
from flask import jsonify
from flask_cors import CORS
import redis
import json
import datetime
import scholarly as sch

app = Flask(__name__)
CORS(app)

cache = redis.StrictRedis(db=0, host='redis-db', port=6379)

@app.route('/author/<string:author>', defaults={'affiliation': None})
@app.route('/author/<string:author>/affiliation/<string:affiliation>')
def search(
    author,
    affiliation,
):
    query = sch.search_author(
        ', '.join((i for i in (author, affiliation) if i))
    )
    first_result = next(query)
    return jsonify({
        'name': first_result.name,
        'affiliation': first_result.affiliation,
        'citedby': first_result.citedby,
        'interests': first_result.interests,
        'url_picture': first_result.url_picture,
    })


if __name__ == '__main__':
    app.run()
