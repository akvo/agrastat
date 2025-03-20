from flask import redirect
from ckan.model import Resource
from ckan.plugins.toolkit import url_for
from ckan.model import meta
from ckan.logic import get_action
from ckanext.agra_theme.models import ResourceDownloadCount


def page_download(blueprint):
    @blueprint.route("/dataset/<id>/resource/<resource_id>/get/<filename>")
    def track_download(id, resource_id, filename):
        # Increment the download count
        record = ResourceDownloadCount.get_or_create(resource_id)
        record.download_count += 1
        meta.Session.commit()

        # Redirect to the actual resource URL
        resource = Resource.get(resource_id)
        if not resource:
            # Handle case where resource does not exist
            return "Resource not found", 404

        # Update the dataset's download_count
        context = {"ignore_auth": True}
        try:
            dataset = get_action("package_show")(context, {"id": id})
            current_download_count = dataset.get("download_count", 0)
            dataset["download_count"] = current_download_count + 1

            # Update the dataset with the new download_count
            get_action("package_update")(context, dataset)
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error updating dataset download count: {e}")

        # Use CKAN's url_for helper to generate the download URL
        download_url = url_for(
            "resource.download",
            id=id,
            resource_id=resource.id,
            _external=True,
            filename=filename,
        )

        return redirect(download_url)
