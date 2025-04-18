import random
from ckan.plugins import toolkit
from ckan.model import Session
from ckan.model import ResourceView, Resource, Package
from ckan.logic import get_action


def get_random_dashboard_view():
    """
    Fetch all resource views with view_type='dashboard_view' and return one randomly.
    Exclude private datasets if the user is not logged in.
    """
    # Check if the user is logged in
    user_is_logged_in = (
        toolkit.c.user
    )  # Returns the username if logged in, otherwise None

    # Perform a join between resource_view, resource, and package tables
    query = (
        Session.query(
            ResourceView.title.label("view_title"),
            ResourceView.id.label("view_id"),
            ResourceView.resource_id,
            Resource.id.label("resource_id"),
            Resource.name.label("resource_name"),
            Package.name.label("package_name"),
            Package.private,
        )
        .join(Resource, ResourceView.resource_id == Resource.id)
        .join(Package, Resource.package_id == Package.id)
        .filter(ResourceView.view_type == "dashboard_view")
        .filter(Resource.state == "active")
        .filter(Package.state == "active")
    )

    # Exclude private datasets if the user is not logged in
    if not user_is_logged_in:
        query = query.filter(Package.private == False)

    query = query.limit(3)

    # Execute the query
    dashboard_views = query.all()

    if not dashboard_views:
        return None  # No dashboard views found

    selected_views = []
    for view in dashboard_views:
        package_name = view.package_name
        resource_id = view.resource_id
        resource_name = view.resource_name
        view_id = view.view_id
        view_title = view.view_title
        iframe_url = toolkit.url_for(
            "resource.view",
            id=package_name,
            resource_id=resource_id,
            view_id=view_id,
            qualified=True,
        )
        selected_views.append(
            {
                "resource_name": resource_name,
                "package_name": package_name,
                "resource_id": resource_id,
                "view_id": view_id,
                "iframe_url": iframe_url,
                "view_title": view_title,
            }
        )
    return selected_views


def datasets_count():
    # Logic to count datasets
    return Session.query(Package).filter(Package.state == "active").count()


def resources_count():
    # Logic to count resources
    return Session.query(Resource).filter(Resource.state == "active").count()


def get_resource_download_count(resource_id):
    # Logic to count resource downloads
    context = {"ignore_auth": True}
    data_dict = {"id": resource_id, "include_tracking": True}
    result = get_action("resource_show")(context, data_dict)
    return result["tracking_summary"]["total"]


def get_package_download_count(package):
    # Logic to count package downloads
    context = {"ignore_auth": True}
    download_count = 0
    for resource in package["resources"]:
        data_dict = {"id": resource["id"], "include_tracking": True}
        result = get_action("resource_show")(context, data_dict)
        download_count += result["tracking_summary"]["recent"]
    return download_count
