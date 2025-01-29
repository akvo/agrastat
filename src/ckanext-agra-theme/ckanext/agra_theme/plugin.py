import os
import gettext
from flask import Blueprint, render_template, request, abort, jsonify
import ckan.plugins as plugins
import logging
import ckan.plugins.toolkit as toolkit
from .routes.api.agrovoc import api_agrovoc
from .routes.api.countries import api_countries
from .routes.pages.statistic import page_statistic
from .middleware import AgraThemeMiddleware
from .data.countries import countries

# Blueprint
agra_blueprint = Blueprint("agra", __name__)
api_agrovoc(agra_blueprint)
api_countries(agra_blueprint)
page_statistic(agra_blueprint)


class AgraThemePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IMiddleware, inherit=True)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    # plugins.implements(plugins.IDatasetForm)

    def get_helpers(self):
        return {
            "countries": countries,
            "business_lines": [
                "Policy and Advocacy",
                "Sustainable Farming",
                "Gender and Youth",
                "Cessa",
                "IMTF",
                "Monitoring and Evaluation",
            ],
            "data_sources": ["Internal", "External"],
            "methodologies": [
                "Primary Data Collection",
                "Secondary Data",
            ],
            "updating_schedules": [
                "Regular",
                "One off",
                "Monthly",
                "Daily",
            ],
        }

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
