import logging
from collections import OrderedDict
from flask import Blueprint, render_template, request, abort, jsonify
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model import meta
from .routes.api.agrovoc import api_agrovoc
from .routes.api.countries import api_countries
from .routes.api.stats import api_stats
from .routes.pages.statistic import page_statistic
from .routes.pages.external import page_external

# from .middleware import AgraThemeMiddleware
from .data.countries import country_list, create_countries
from .data.value_chain import value_chain_list, create_value_chains
from .data.business_line import business_line_list, create_business_lines
from .data.impact_area import impact_area_list, create_impact_areas
from .cli import agra as agra_cli
from .helpers import (
    get_random_dashboard_view,
    datasets_count,
    resources_count,
    get_resource_download_count,
    get_package_download_count,
)

log = logging.getLogger(__name__)

# Blueprint
agra_blueprint = Blueprint("agra", __name__)
api_agrovoc(agra_blueprint)
api_countries(agra_blueprint)
api_stats(agra_blueprint)
page_statistic(agra_blueprint)
page_external(agra_blueprint)

schema_names = [
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
create_value_chains()
create_business_lines()
create_impact_areas()


class AgraThemePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    # plugins.implements(plugins.IMiddleware, inherit=True)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IClick)

    def get_helpers(self):
        return {
            "countries": country_list,
            "value_chains": value_chain_list,
            "business_lines": business_line_list,
            "impact_areas": impact_area_list,
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
            "facet_disabled": ["license_id"],
            "get_random_dashboard_view": get_random_dashboard_view,
            "datasets_count": datasets_count,
            "resources_count": resources_count,
            "get_resource_download_count": get_resource_download_count,
            "get_package_download_count": get_package_download_count,
        }

    # IClick (CLI)
    def get_commands(self):
        return [agra_cli]

    def before_index(self, data_dict):
        extras = data_dict.get("extras", {})
        log.info(f"Before index - Original Extras: {extras}")
        for key, value in extras.items():
            data_dict[f"extras_{key}"] = value
        return data_dict

    def modify_facets(self, facets_dict, unlisted=[]):
        if not facets_dict:
            facets_dict = {}

        # Remove unwanted facets
        for filter_facet in unlisted:
            facets_dict.pop(filter_facet, None)
        facets_dict.pop("license_id", None)

        # Define the new order
        vocab_keys = {  # Ensure vocab keys come first
            "vocab_business_lines": toolkit._("Business Lines"),
            "vocab_impact_areas": toolkit._("Impact Areas"),
            "vocab_value_chains": toolkit._("Value Chains"),
            "vocab_countries": toolkit._("Countries"),
            "tags": facets_dict.get("tags"),
        }

        # Create an ordered dictionary
        ordered_facets = OrderedDict()

        # Add vocab facets first
        ordered_facets.update(vocab_keys)

        # Add remaining facets (except tags) in the original order
        for key, value in facets_dict.items():
            if key not in vocab_keys and key != "tags":
                ordered_facets[key] = value

        return ordered_facets

    def dataset_facets(self, facets_dict, package_type):
        return self.modify_facets(facets_dict)

    def organization_facets(
        self, facets_dict, organization_type, package_type
    ):
        return self.modify_facets(facets_dict, unlisted=["organization"])

    def group_facets(self, facets_dict, group_type, package_type):
        return self.modify_facets(facets_dict, unlisted=["groups"])

    def get_blueprint(self):
        return agra_blueprint

    # def make_middleware(self, app, config):
    #     # Wrap the CKAN app with our custom middleware
    #     return AgraThemeMiddleware(app)

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
                ],
                "value_chains": [
                    toolkit.get_validator("not_empty"),
                    toolkit.get_converter("convert_to_tags")("value_chains"),
                ],
                "business_lines": [
                    toolkit.get_validator("not_empty"),
                    toolkit.get_converter("convert_to_tags")("business_lines"),
                ],
                "impact_areas": [
                    toolkit.get_validator("not_empty"),
                    toolkit.get_converter("convert_to_tags")("impact_areas"),
                ],
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
        schema.update(
            {
                "download_count": [toolkit.get_validator("ignore_missing")],
            }
        )
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
                ],
                "value_chains": [
                    toolkit.get_converter("convert_from_tags")("value_chains"),
                    toolkit.get_validator("ignore_missing"),
                ],
                "business_lines": [
                    toolkit.get_converter("convert_from_tags")(
                        "business_lines"
                    ),
                    toolkit.get_validator("ignore_missing"),
                ],
                "impact_areas": [
                    toolkit.get_converter("convert_from_tags")("impact_areas"),
                    toolkit.get_validator("ignore_missing"),
                ],
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
        schema.update(
            {
                "download_count": [toolkit.get_validator("ignore_missing")],
            }
        )
        return schema
