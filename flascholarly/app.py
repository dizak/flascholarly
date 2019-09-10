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

try:
    cache.info()
except redis.exceptions.ConnectionError:
    cache = None


@app.route('/author/<string:author>', defaults={'affiliation': None})
@app.route('/author/<string:author>/affiliation/<string:affiliation>')
def search(
    author,
    affiliation,
):
    if cache:
        first_result_json = cache.get('{}+{}'.format(
            author,
            affiliation,
        ))
        if first_result_json:
            return first_result_json
    query = sch.search_author(
        ', '.join((i for i in (author, affiliation) if i))
    )
    results = list(query)
    if not results:
        return 'No record found'
    results_l = []
    for i in results:
        results_d = {}
        if hasattr(i, 'name'): results_d['name'] = i.name
        if hasattr(i, 'affiliation'): results_d['affiliation'] = i.affiliation
        if hasattr(i, 'author'): results_d['author'] = i.author
        if hasattr(i, 'citedby'): results_d['citedby'] = i.citedby
        if hasattr(i, 'interests'): results_d['interests'] = i.interests
        if hasattr(i, 'url_picture'): results_d['url_picture'] = i.url_picture
        results_l.append(results_d)
    return jsonify(results_l)
    first_result = results[0]
    first_result_dict = {
        'name': first_result.name,
        'affiliation': first_result.affiliation,
        'citedby': first_result.citedby,
        'interests': first_result.interests,
        'url_picture': first_result.url_picture,
    }
    if cache:
        cache.set(
            '{}+{}'.format(author, affiliation),
            json.dumps(first_result_dict),
        )
        cache.pexpire(
            '{}+{}'.format(author, affiliation),
            datetime.timedelta(days=1),
        )
    return jsonify(first_result_dict)


if __name__ == '__main__':
    app.run()
