from flask import Flask, jsonify
from flask_restful import Resource, Api

import webscrape

app = Flask(__name__)
api = Api(app)

class WebScrape(Resource):
    def get(self):
        return jsonify(webscrape.get_special_menu_json())

api.add_resource(WebScrape, '/specials/webscrape')

if __name__ == '__main__':
    app.run(threaded=True, port=5000)