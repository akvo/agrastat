import requests
from flask import jsonify, request

countries_json = "https://gist.githubusercontent.com/almost/7748738/raw/575f851d945e2a9e6859fb2308e95a3697bea115/countries.json"
countries = requests.get(countries_json).json()


def api_countries(blueprint):
    @blueprint.route("/api/2/util/countries", methods=["GET"])
    def countries_list():
        return jsonify(countries)
