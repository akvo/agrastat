import requests
import ckan.plugins.toolkit as toolkit


def page_statistic(blueprint):
    @blueprint.route("/dataset/<dataset_id>/file_size")
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
        return toolkit.render(
            "file_size.html", {"resource_sizes": resource_sizes}
        )
