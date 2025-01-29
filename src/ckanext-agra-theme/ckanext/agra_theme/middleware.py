from os import environ
from flask import Response


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
            ".tsv",
            ".json",
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
