import random
from ckan.plugins import toolkit
from ckan.model import Session
from ckan.model import ResourceView, Resource, Package


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
    )

    # Exclude private datasets if the user is not logged in
    if not user_is_logged_in:
        query = query.filter(Package.private == False)

    # Execute the query
    dashboard_views = query.all()

    if not dashboard_views:
        return None  # No dashboard views found

    # Randomly select one view
    selected_view = random.choice(dashboard_views)

    # Extract package name, resource ID, and view ID
    package_name = selected_view.package_name
    resource_id = selected_view.resource_id
    resource_name = selected_view.resource_name
    view_id = selected_view.view_id

    # Construct the full iframe URL
    iframe_url = toolkit.url_for(
        "resource.view",
        id=package_name,
        resource_id=resource_id,
        view_id=view_id,
        qualified=True,
    )

    # Return the view details
    return {
        "resource_name": resource_name,
        "package_name": package_name,
        "resource_id": resource_id,
        "view_id": view_id,
        "iframe_url": iframe_url,
    }
