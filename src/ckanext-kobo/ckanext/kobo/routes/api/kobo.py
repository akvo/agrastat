import requests as req
from flask import jsonify, make_response
from ckan import model
from ckanext.kobo.model import Kobo
from ckan.model.resource import Resource


# Example Data
# package_id = Column(types.UnicodeText, ForeignKey("package.id"))
# export_settings_uid = Column(types.String(255))
# asset_uid = Column(types.String(255))
# kobo_token = Column(types.String(255))
# kf_url = Column(types.String(255))
# next_run = Column(types.DateTime)
# last_run = Column(types.DateTime)
# package = relationship(Package, backref=backref("kobo", uselist=False))


def download_kobo_data(kb):
    full_url = "{}/api/v2/assets/{}/export-settings/{}/data.csv".format(
        kb.get("kf_url"),
        kb.get("asset_uid"),
        kb.get("export_settings_uid"),
    )
    headers = {"Authorization": "Token {}".format(kb.get("kobo_token"))}
    res = req.get(full_url, headers=headers)
    if res:
        # replace ; delimiter to comma
        csv_string = (
            res.text.replace('";"', '","').replace("__", "").replace('"_', '"')
        )
        response = make_response(csv_string)
        response.headers[
            "Content-Disposition"
        ] = "attachment; filename=data.csv"
        response.headers["Content-Type"] = "text/csv"
        return response
    return jsonify({"error": "Couldn't fetch"}), 500


def api_kobo(blueprint):
    @blueprint.route("/api/2/kobo/<asset_uid>", methods=["GET"])
    def get_by_resource_id(asset_uid):
        res = (
            model.Session.query(Resource)
            .filter(Resource.hash == asset_uid)
            .first()
        )
        if res:
            return download_kobo_data(res.extras)
        else:
            return jsonify({"error": "Resource not found"}), 404
