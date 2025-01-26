import logging
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy.orm import backref, relationship
from sqlalchemy.exc import InvalidRequestError

from ckan.model.meta import Session
from ckan.model.types import make_uuid
from ckan.model.domain_object import DomainObject
from ckan.model.resource import Resource


try:
    from ckan.model.toolkit import BaseModel
except ImportError:
    from ckan.model.meta import metadata
    from sqlalchemy.ext.declarative import declarative_base

    BaseModel = declarative_base(metadata=metadata)


log = logging.getLogger(__name__)


class KoboObject(DomainObject):

    key_attr = "id"

    @classmethod
    def get(cls, key, default=None, attr=None):
        if attr is None:
            attr = cls.key_attr
        kwds = {attr: key}
        obj = cls.filter(**kwds).first()
        if obj:
            return obj
        return default

    @classmethod
    def filter(cls, **kwds):
        query = Session.query(cls).autoflush(False)
        return query.filter_by(**kwds)


class Kobo(BaseModel, KoboObject):
    __tablename__ = "kobo"

    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    resource_id = Column(types.UnicodeText, ForeignKey("resource.id"))
    export_settings_uid = Column(types.String(255))
    asset_uid = Column(types.String(255))
    kobo_token = Column(types.String(255))
    kf_url = Column(types.String(255))
    next_run = Column(types.DateTime)
    last_run = Column(types.DateTime)

    # Added fields
    status = Column(
        types.String(50), default="inactive"
    )  # e.g., 'active', 'inactive', 'error'
    error_message = Column(types.UnicodeText)
    last_successful_run = Column(types.DateTime)
    update_frequency = Column(
        types.String(50)
    )  # e.g., 'daily', 'weekly', 'hourly'

    resource = relationship(Resource, backref=backref("kobo", uselist=False))

    def __init__(
        self,
        resource_id,
        export_settings_uid,
        asset_uid,
        kobo_token,
        kf_url,
        next_run,
        last_run,
        status="inactive",  # New field with default
        error_message=None,  # New field
        last_successful_run=None,  # New field
        update_frequency=None,  # New field
    ):
        self.resource_id = resource_id
        self.export_settings_uid = export_settings_uid
        self.asset_uid = asset_uid
        self.kobo_token = kobo_token
        self.kf_url = kf_url
        self.next_run = next_run
        self.last_run = last_run
        self.status = status
        self.error_message = error_message
        self.last_successful_run = last_successful_run
        self.update_frequency = update_frequency

    def __repr__(self):
        return (
            "<Kobo id=%s resource_id=%s kf_url=%s asset_uid=%s status=%s>"
            % (
                self.id,
                self.resource_id,
                self.kf_url,
                self.asset_uid,
                self.status,  # Include status in representation
            )
        )

    def __str__(self):
        return self.__repr__().encode("ascii", "ignore")

    def to_dict(self):
        data = {
            "id": self.id,
            "resource_id": self.resource_id,
            "export_settings_uid": self.export_settings_uid,
            "asset_uid": self.asset_uid,
            "kobo_token": self.kobo_token,
            "kf_url": self.kf_url,
            "next_run": self.next_run,
            "last_run": self.last_run,
            "resource": self.resource.name if self.resource else None,
            # Add new fields to the dictionary
            "status": self.status,
            "error_message": self.error_message,
            "last_successful_run": self.last_successful_run,
            "update_frequency": self.update_frequency,
        }
        return data

    @classmethod
    def get(cls, resource_id):
        return cls.filter(resource_id=resource_id).first()

    @classmethod
    def create(
        cls,
        resource_id,
        export_settings_uid,
        asset_uid,
        kobo_token,
        kf_url,
        next_run,
        last_run,
        status="inactive",  # New field with default
        error_message=None,  # New field
        last_successful_run=None,  # New field
        update_frequency=None,  # New field
    ):
        obj = cls(
            resource_id,
            export_settings_uid,
            asset_uid,
            kobo_token,
            kf_url,
            next_run,
            last_run,
            status,
            error_message,
            last_successful_run,
            update_frequency,
        )
        Session.add(obj)
        Session.commit()
        return obj

    @classmethod
    def update(
        cls,
        resource_id,
        export_settings_uid,
        asset_uid,
        kobo_token,
        kf_url,
        next_run,
        last_run,
        status="inactive",  # New field with default
        error_message=None,  # New field
        last_successful_run=None,  # New field
        update_frequency=None,  # New field
    ):
        obj = cls.get(resource_id)
        if obj:
            obj.export_settings_uid = export_settings_uid
            obj.asset_uid = asset_uid
            obj.kobo_token = kobo_token
            obj.kf_url = kf_url
            obj.next_run = next_run
            obj.last_run = last_run
            # Update new fields
            obj.status = status
            obj.error_message = error_message
            obj.last_successful_run = last_successful_run
            obj.update_frequency = update_frequency
            Session.commit()
            return obj
        return None

    @classmethod
    def delete(cls, resource_id):
        obj = cls.get(resource_id)
        if obj:
            Session.delete(obj)
            Session.commit()
            return obj
        return None

    @classmethod
    def all(cls):
        return cls.filter().all()
