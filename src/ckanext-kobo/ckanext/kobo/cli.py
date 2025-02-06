import click
import subprocess
from ckan.model import Session
from ckan.model.resource import Resource
from ckan.plugins.toolkit import config


@click.group(name="kobo")
def kobo():
    """CKAN CLI commands for Kobo integration"""
    pass


@kobo.command(name="resubmit")
@click.option(
    "--resource-id",
    default=None,
    help="Specific resource ID to resubmit. If blank, resubmits all.",
)
def resubmit(resource_id):
    """Finds resources with url_type='kobo' and resubmits them to the DataPusher"""
    session = Session()

    if resource_id:
        # Resubmit a single resource
        resource = (
            session.query(Resource.id)
            .filter(Resource.id == resource_id, Resource.url_type == "kobo")
            .first()
        )
        if not resource:
            click.echo(
                f"Resource {resource_id} not found or not of type 'kobo'."
            )
            return
        resources = [(resource.id,)]
    else:
        # Resubmit all Kobo resources
        resources = (
            session.query(Resource.id).filter(Resource.url_type == "kobo").all()
        )

    if not resources:
        click.echo("No Kobo resources found.")
        return

    click.echo(f"Found {len(resources)} Kobo resource(s). Resubmitting...")

    for (res_id,) in resources:
        cmd = ["ckan", "datapusher", "resubmit", res_id]
        click.echo(f"Running: {' '.join(cmd)}")

        try:
            subprocess.run(cmd, check=True)
            click.echo(f"Successfully resubmitted {res_id}")
        except subprocess.CalledProcessError as e:
            click.echo(f"Failed to resubmit {res_id}: {e}")
