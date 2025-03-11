import json
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from .schema import schema


class DashboardViewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    def get_helpers(self):
        return {}

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("fanstatic", "dashboard_view")

    def info(self):
        return {
            "name": "dashboard_view",
            "title": "Dashboard View",
            "icon": "dashboard",
            "requires_datastore": True,
            "schema": schema,
            "default_title": "Dashboard View",
        }

    def can_view(self, data_dict):
        resource = data_dict["resource"]
        return resource.get(
            "datastore_active"
        ) or "_datastore_only_resource" in resource.get("url", "")

    def setup_template_variables(self, context, data_dict):
        return {
            "resource_json": json.dumps(data_dict["resource"]),
            "resource_view_json": json.dumps(data_dict["resource_view"]),
        }

    def view_template(self, context, data_dict):
        return "dashboard_view.html"

    def form_template(self, context, data_dict):
        return "dashboard_view_form.html"
