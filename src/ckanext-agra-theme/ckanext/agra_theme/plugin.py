from os import environ
from werkzeug.wrappers import Response, Request
from flask import Blueprint, render_template, request, abort, jsonify
import ckan.plugins as plugins
import requests
import logging
import ckan.plugins.toolkit as toolkit
from .routes.api.agrovoc import api_agrovoc
from .routes.api.countries import api_countries
from .routes.pages.statistic import page_statistic

# Blueprint
agra_blueprint = Blueprint("agra", __name__)
api_agrovoc(agra_blueprint)
api_countries(agra_blueprint)
page_statistic(agra_blueprint)


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
