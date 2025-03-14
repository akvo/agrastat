import json
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

ignore_empty = plugins.toolkit.get_validator("ignore_empty")


class DashboardViewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    def get_resource_parameters(self, data_dict):
        # Get the resource ID
        resource_id = data_dict["resource"]["id"]

        try:
            # Fetch column metadata from the DataStore
            datastore_info = toolkit.get_action("datastore_search")(
                {},  # Empty context
                {
                    "resource_id": resource_id,
                    "limit": 0,
                },  # No rows needed, just metadata
            )
            # Extract fields (columns) and their types
            columns = [
                {"name": field["id"], "type": field["type"]}
                for field in datastore_info.get("fields", [])
            ]
        except Exception as e:
            # Handle errors (e.g., if DataStore is not enabled or resource not in DataStore)
            columns = []
            print(f"Error fetching DataStore metadata: {e}")

        return columns

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
            "schema": {"columns": [ignore_empty]},
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
        if data_dict["resource_view"].get("columns"):
            try:
                data_dict["columns"] = json.loads(
                    data_dict["resource_view"]["columns"]
                )
            except json.JSONDecodeError:
                data_dict["columns"] = []
        return "dashboard_view.html"

    def form_template(self, context, data_dict):
        data_dict["data_columns"] = self.get_resource_parameters(data_dict)
        return "dashboard_view_form.html"
