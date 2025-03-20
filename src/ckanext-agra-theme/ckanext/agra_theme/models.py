from sqlalchemy import Table, Column, Integer, UnicodeText, ForeignKey
from sqlalchemy.orm import mapper, relationship
from ckan.model import meta, Resource

# Define the table schema
resource_download_count_table = Table(
    "resource_download_count",  # Table name
    meta.metadata,  # Use CKAN's global metadata
    Column("id", Integer, primary_key=True),
    Column(
        "resource_id", UnicodeText, ForeignKey("resource.id"), nullable=False
    ),
    Column("download_count", Integer, default=0),
)

# Define the Python class
class ResourceDownloadCount(object):
    def __init__(self, resource_id, download_count=0):
        self.resource_id = resource_id
        self.download_count = download_count

    @classmethod
    def get_or_create(cls, resource_id):
        obj = (
            meta.Session.query(cls).filter_by(resource_id=resource_id).first()
        )
        if not obj:
            obj = cls(resource_id=resource_id)
        meta.Session.add(obj)  # Add or update the object
        meta.Session.commit()  # Commit changes to the database
        return obj


# Map the class to the table
mapper(
    ResourceDownloadCount,
    resource_download_count_table,
    properties={"resource": relationship(Resource, backref="download_count")},
)


def get_resource_download_count(resource_id):
    """
    Helper function to retrieve the download count for a given resource_id.

    :param resource_id: The ID of the resource.
    :return: The download count as an integer, or 0 if no record exists or an error occurs.
    """
    try:
        record = (
            meta.Session.query(ResourceDownloadCount)
            .filter_by(resource_id=resource_id)
            .first()
        )
        return record.download_count if record else 0
    except Exception as e:
        # Log the error and return 0
        from ckan.plugins.toolkit import log

        log.error(
            f"Error retrieving download count for resource {resource_id}: {str(e)}"
        )
        return 0
