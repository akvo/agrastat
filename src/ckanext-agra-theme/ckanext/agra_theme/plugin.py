from flask import Blueprint, render_template, request, abort, jsonify
import ckan.plugins as plugins
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

extra_fields = [
    "business_line",
    "source",
    "country",
    "methodology",
    "pii",
    "anon",
]


class AgraThemePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IMiddleware, inherit=True)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IDatasetForm, inherit=False)

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

    # IDatasetForm
    def is_fallback(self):
        """Indicates that this is not the fallback dataset schema."""
        return True

    def package_types(self):
        """Specify the package types that this form should handle."""
        return ["dataset"]

    def _modify_schema(self, schema):
        for new_field in extra_fields:
            schema.update(
                {
                    new_field: [
                        toolkit.get_validator("ignore_missing"),
                        toolkit.get_converter("convert_to_extras"),
                    ]
                }
            )
        return schema

    def create_package_schema(self):
        """Return the schema for package creation."""
        schema = super(AgraThemePlugin, self).create_package_schema()
        return self._modify_schema(schema)

    def update_package_schema(self):
        """Return the schema for package updates."""
        schema = super(AgraThemePlugin, self).update_package_schema()
        return self._modify_schema(schema)

    def show_package_schema(self):
        """Return the schema for package display."""
        schema = super(AgraThemePlugin, self).show_package_schema()
        return self._modify_schema(schema)
