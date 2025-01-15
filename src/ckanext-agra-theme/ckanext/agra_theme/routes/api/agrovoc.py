import requests
from flask import jsonify, request, abort

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
min_query_length = 3
agrovoc_url = "https://agrovoc.fao.org"
agrovoc_search_url = f"{agrovoc_url}/browse/rest/v1/search"
agrovoc_suggestion_url = f"{agrovoc_url}/browse/rest/v1/agrovoc/"


def api_agrovoc(blueprint):
    @blueprint.route("/api/2/util/tag/suggestion", methods=["GET"])
    def autocomplete():
        # Get the 'q' query parameter from the request
        q = request.args.get("q", "")
        category = request.args.get("category", "broader")
        if not q:
            return abort(404)
        if len(q) < min_query_length:
            return abort(404)

        # Call the AGROVOC API
        # https://www.fao.org/agrovoc/machine-use
        search_url = f"{agrovoc_search_url}?query={q}*&{agrovoc_query}"
        res = requests.get(search_url)

        # Check if the AGROVOC API call was successful
        if res.status_code != 200:
            return abort(404)
        agrovoc_data = res.json()
        content_url = agrovoc_data.get("results")
        if content_url:
            content_url = content_url[0].get("uri", "")
        else:
            return abort(404)
        res = requests.get(
            f"{agrovoc_suggestion_url}{category}?uri={content_url}"
        )
        agrovoc_suggestion_data = res.json()

        data_key = "broader"
        if category == "children":
            data_key = "narrower"

        # Transform the AGROVOC API response to CKAN's expected format
        results = [
            result.get("prefLabel", "")
            for result in agrovoc_suggestion_data.get(data_key, [])
            if "prefLabel" in result
        ]

        return jsonify(results)
