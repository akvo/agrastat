from os import environ
from werkzeug.wrappers import Response, Request
from flask import Blueprint, render_template, abort
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging

file_size_blueprint = Blueprint("file_size", __name__)


@file_size_blueprint.route("/dataset/<dataset_id>/file_size")
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
            {"name": resource.get("name"), "size": size if size else "Unknown"}
        )

    # Render a template with the resource size data
    return toolkit.render("file_size.html", {"resource_sizes": resource_sizes})


class AgraThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IMiddleware, inherit=True)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IRoutes, inherit=True)

    def get_blueprint(self):
        return file_size_blueprint

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
            "/user/reset",  # Reset password page
            "/about",
        ]
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
