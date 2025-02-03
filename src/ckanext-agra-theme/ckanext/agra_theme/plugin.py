from flask import Blueprint, render_template, request, abort, jsonify
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from .routes.api.agrovoc import api_agrovoc
from .routes.api.countries import api_countries
from .routes.pages.statistic import page_statistic
from .middleware import AgraThemeMiddleware
from .data.countries import country_list, create_countries

# Blueprint
agra_blueprint = Blueprint("agra", __name__)
api_agrovoc(agra_blueprint)
api_countries(agra_blueprint)
page_statistic(agra_blueprint)

schema_names = [
    {"name": "business_line", "required": True},
    {"name": "data_source", "required": True},
    {
        "name": "methodology",
        "required": False,
    },
    {
        "name": "legal",
        "required": False,
    },
    {
        "name": "sharing_agreement",
        "required": False,
    },
    {
        "name": "pii",
        "required": True,
    },
    {
        "name": "anon",
        "required": True,
    },
    {
        "name": "updating_schedule",
        "required": False,
    },
]

create_countries()


class AgraThemePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IMiddleware, inherit=True)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IDatasetForm)

    def get_helpers(self):
        return {
            "countries": country_list,
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

    def _modify_package_schema(self, schema):
        schema.update(
            {
                "countries": [
                    toolkit.get_validator("not_empty"),
                    toolkit.get_converter("convert_to_tags")("countries"),
                ]
            }
        )
        for schema_name in schema_names:
            schema.update(
                {
                    schema_name["name"]: [
                        toolkit.get_validator("not_empty")
                        if schema_name["required"]
                        else toolkit.get_validator("ignore_missing"),
                        toolkit.get_converter("convert_to_extras"),
                    ]
                }
            )
        return schema

    def create_package_schema(self):
        """Return the schema for package creation."""
        schema = super(AgraThemePlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        """Return the schema for package updates."""
        schema = super(AgraThemePlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        """Return the schema for package display."""
        schema = super(AgraThemePlugin, self).show_package_schema()
        # (e.g. on dataset pages, or on the search page)
        schema["tags"]["__extras"].append(
            toolkit.get_converter("free_tags_only")
        )

        # Add our custom country_code metadata field to the schema.
        schema.update(
            {
                "countries": [
                    toolkit.get_converter("convert_from_tags")("countries"),
                    toolkit.get_validator("ignore_missing"),
                ]
            }
        )
        for schema_name in schema_names:
            schema.update(
                {
                    schema_name["name"]: [
                        toolkit.get_converter("convert_from_extras"),
                        toolkit.get_validator("ignore_missing"),
                    ]
                }
            )
        return schema
