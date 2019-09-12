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
try:
    from . import utils
except ImportError:
    import utils

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
    ordered_author = utils.order_author(author)
    if cache:
        first_result_json = cache.get('{}+{}'.format(
            ordered_author,
            affiliation,
        ))
        if first_result_json:
            return first_result_json
    query = sch.search_ordered_author(
        ', '.join((i for i in (ordered_author, affiliation) if i))
    )
    results = [i.__dict__ for i in query]
    if not results:
        return 'No record found'
    for i in results:
        del i['_filled']
    if cache:
        cache.set(
            '{}+{}'.format(ordered_author, affiliation),
            json.dumps(results),
        )
        cache.pexpire(
            '{}+{}'.format(ordered_author, affiliation),
            datetime.timedelta(days=1),
        )
    return jsonify(results)


if __name__ == '__main__':
    app.run()
