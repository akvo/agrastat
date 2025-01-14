from os import environ
from werkzeug.wrappers import Response, Request
from flask import Blueprint, render_template, request, abort, jsonify
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import requests
import logging


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

# Extra Dataset
ignore_missing = toolkit.get_validator("ignore_missing")
not_empty = toolkit.get_validator("not_empty")


def dataset_schema():
    schema = {
        "extras": {
            "country": [ignore_missing],
        },
    }
    return schema


# Blueprint
agra_blueprint = Blueprint("agra", __name__)
countries_json = "https://gist.githubusercontent.com/almost/7748738/raw/575f851d945e2a9e6859fb2308e95a3697bea115/countries.json"
countries = requests.get(countries_json).json()


@agra_blueprint.route("/api/countries", methods=["GET"])
def search_countries():
    # Get the query parameter
    query = request.args.get("q", "").lower()
    if query:
        # Filter countries by query
        filtered_countries = [
            country for country in countries if query in country["name"].lower()
        ]
    else:
        # Return all countries if no query is provided
        filtered_countries = countries

    # Return JSON response
    return jsonify(filtered_countries)


@agra_blueprint.route("/api/2/util/tag/autocomplete", methods=["GET"])
def agrovoc_search():
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


@agra_blueprint.route("/dataset/<dataset_id>/file_size")
def file_size(dataset_id):
    # Set up the context for accessing CKAN actions
    context = {"user": toolkit.g.user}

    try:
        # Retrieve the dataset and its resources using CKAN actions
        dataset = toolkit.get_action("package_show")(
            context, {"id": dataset_id}
        )
        resources = dataset["resources"]
    except toolkit.ObjectNotFound:
        abort(404, description="Dataset not found")

    # Prepare a list to store resource file sizes
    resource_sizes = []
    for resource in resources:
        size = resource.get("size")

        # If the size is None, try to retrieve it from the URL
        if not size:
            url = resource.get("url")
            try:
                response = requests.head(url, allow_redirects=True)
                size = response.headers.get("Content-Length")
            except requests.RequestException:
                size = None

        # Append to list with resource name and size
        resource_sizes.append(
            {
                "name": resource.get("name"),
                "size": size if size else "Unknown",
            }
        )

    # Render a template with the resource size data
    return toolkit.render("file_size.html", {"resource_sizes": resource_sizes})


class AgraThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IMiddleware, inherit=True)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IRoutes, inherit=True)

    def get_blueprint(self):
        return agra_blueprint

    def make_middleware(self, app, config):
        # Wrap the CKAN app with our custom middleware
        return AgraThemeMiddleware(app)

    # IConfigurer
    def update_config(self, config_):
        # Add the template, public, and resource directories for the theme
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("fanstatic", "agra_theme")


class AgraThemeMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Check if the user is logged in based on the presence of 'REMOTE_USER'
        user = environ.get("REMOTE_USER")

        # Define allowed paths for non-logged-in users
        path = environ.get("PATH_INFO", "")
        allowed_paths = [
            "/",  # Home page
            "/user/login",  # Login page
            "/about",
        ]
        # start with "/user/reset"
        if path.startswith("/user/reset"):
            return self.app(environ, start_response)

        resource_paths = ["/base/", "/public/", "/fanstatic/"]
        allowed_path_keywords = ["/api/"]
        allowed_resource = [
            ".jpg",
            ".png",
            ".css",
            ".js",
            ".csv",
            ".xls",
            ".xlsx",
        ]

        if path.startswith(tuple(resource_paths)) or path.endswith(
            tuple(allowed_resource)
        ):
            return self.app(environ, start_response)

        if any(keyword in path for keyword in allowed_path_keywords):
            return self.app(environ, start_response)

        # Redirect non-logged-in users trying to access any other page
        if not user and path not in allowed_paths:
            # Create a redirect response to the login page
            response = Response("Redirecting to login...", status=302)
            response.headers["Location"] = "/user/login"
            return response(environ, start_response)

        # Continue with the original request if logged in or on an allowed path
        return self.app(environ, start_response)
