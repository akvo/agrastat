import requests
from flask import jsonify, request

# Constants
agrovoc_params = {
    "maxhits": 1,
    "lang": "en",
    "labellang": "en",
    "vocab": "agrovoc",
    "unique": "true",
    "type": "skos:Concept",
}
agrovoc_query = "&".join(
    [f"{key}={value}" for key, value in agrovoc_params.items()]
)
min_query_length = 1
agrovoc_url = "https://agrovoc.fao.org"
agrovoc_search_url = f"{agrovoc_url}/browse/rest/v1/search"
agrovoc_child_url = f"{agrovoc_url}/browse/rest/v1/agrovoc/children?uri="


def api_agrovoc(blueprint):
    @blueprint.route("/api/2/util/tag/autocomplete", methods=["GET"])
    def autocomplete():
        # Get the 'incomplete' query parameter from the request
        incomplete = request.args.get("incomplete", "")
        if not incomplete:
            return jsonify({"ResultSet": {"Result": []}})
        if len(incomplete) < min_query_length:
            return jsonify({"ResultSet": {"Result": []}})

        # Call the AGROVOC API
        # https://www.fao.org/agrovoc/machine-use
        search_url = f"{agrovoc_search_url}?query={incomplete}*&{agrovoc_query}"
        response = requests.get(search_url)

        # Check if the AGROVOC API call was successful
        if response.status_code != 200:
            return jsonify({"ResultSet": {"Result": []}})

        agrovoc_data = response.json()
        content_url = agrovoc_data.get("results")[0].get("uri", "")
        response = requests.get(f"{agrovoc_child_url}{content_url}")
        agrovoc_child_data = response.json()

        # Transform the AGROVOC API response to CKAN's expected format
        results = [
            {"Name": result.get("prefLabel", "")}
            for result in agrovoc_child_data.get("narrower", [])
            if "prefLabel" in result
        ]

        return jsonify({"ResultSet": {"Result": results}})
