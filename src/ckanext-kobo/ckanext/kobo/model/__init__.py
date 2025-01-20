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
from ckan.model.package import Package


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
    package_id = Column(types.UnicodeText, ForeignKey("package.id"))
    export_settings_uid = Column(types.String(255))
    asset_uid = Column(types.String(255))
    kobo_token = Column(types.String(255))
    kf_url = Column(types.String(255))
    next_run = Column(types.DateTime)
    last_run = Column(types.DateTime)
    package = relationship(Package, backref=backref("kobo", uselist=False))

    def __init__(
        self,
        package_id,
        export_settings_uid,
        asset_uid,
        kobo_token,
        kf_url,
        next_run,
        last_run,
    ):
        self.package_id = package_id
        self.export_settings_uid = export_settings_uid
        self.asset_uid = asset_uid
        self.kobo_token = kobo_token
        self.kf_url = kf_url
        self.next_run = next_run
        self.last_run = last_run

    def __repr__(self):
        return "<Kobo id=%s package_id=%s kf_url=%s asset_uid=%s>" % (
            id,
            self.package_id,
            self.kf_url,
            self.asset_uid,
        )

    def __str__(self):
        return self.__repr__().encode("ascii", "ignore")

    def to_dict(self):
        return {
            "id": self.id,
            "package_id": self.package_id,
            "export_settings_uid": self.export_settings_uid,
            "asset_uid": self.asset_uid,
            "kobo_token": self.kobo_token,
            "kf_url": self.kf_url,
            "next_run": self.next_run,
            "last_run": self.last_run,
            "package": self.package.name if self.package else None,
        }

    @classmethod
    def get(cls, package_id):
        return cls.filter(package_id=package_id).first()

    @classmethod
    def create(
        cls,
        package_id,
        export_settings_uid,
        asset_uid,
        kobo_token,
        kf_url,
        next_run,
        last_run,
    ):
        obj = cls(
            package_id,
            export_settings_uid,
            asset_uid,
            kobo_token,
            kf_url,
            next_run,
            last_run,
        )
        Session.add(obj)
        Session.commit()
        return obj

    @classmethod
    def update(
        cls,
        package_id,
        export_settings_uid,
        asset_uid,
        kobo_token,
        kf_url,
        next_run,
        last_run,
    ):
        obj = cls.get(package_id)
        if obj:
            obj.export_settings_uid = export_settings_uid
            obj.asset_uid = asset_uid
            obj.kobo_token = kobo_token
            obj.kf_url = kf_url
            obj.next_run = next_run
            obj.last_run = last_run
            Session.commit()
            return obj
        return None

    @classmethod
    def delete(cls, package_id):
        obj = cls.get(package_id)
        if obj:
            Session.delete(obj)
            Session.commit()
            return obj
        return None

    @classmethod
    def all(cls):
        return cls.filter().all()
