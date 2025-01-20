from flask import jsonify
from ckan import model
from ckanext.kobo.model import Kobo
from ckan.model import Package

# Example Data
# package_id = Column(types.UnicodeText, ForeignKey("package.id"))
# export_settings_uid = Column(types.String(255))
# asset_uid = Column(types.String(255))
# kobo_token = Column(types.String(255))
# kf_url = Column(types.String(255))
# next_run = Column(types.DateTime)
# last_run = Column(types.DateTime)
# package = relationship(Package, backref=backref("kobo", uselist=False))


def api_kobo(blueprint):
    @blueprint.route("/api/2/kobo", methods=["GET"])
    def get_all():
        all_kobos = model.Session.query(Kobo).all()
        return jsonify([a.to_dict() for a in all_kobos])
