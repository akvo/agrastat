import requests as req
import pandas as pd
from flask import jsonify, make_response, request
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
def fetch_all_assets(kb):
    base_url = "{}/api/v2/assets/{}/data.json".format(
        kb.get("kf_url"),
        kb.get("asset_uid"),
    )
    headers = {"Authorization": "Token {}".format(kb.get("kobo_token"))}
    assets = []
    next_url = base_url
    while next_url:
        response = req.get(next_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            assets.extend(data.get("results", []))
            next_url = data.get("next")  # Get the next page URL
        else:
            print(
                f"Failed to fetch data: {response.status_code}, {response.text}"
            )
            break
    return assets


def download_kobo_data(res):
    data = fetch_all_assets(res.extras)
    df = pd.DataFrame(data)
    df = pd.json_normalize(data)
    # replace prefix _ in headers with empty string
    df.columns = df.columns.str.replace("^_+", "", regex=True)
    response = make_response(df.to_csv(index=False))
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


def api_kobo(blueprint):
    @blueprint.route("/api/2/kobo/<asset_uid>", methods=["GET"])
    def get_by_resource_id(asset_uid):
        res = (
            model.Session.query(Resource)
            .filter(Resource.hash == asset_uid)
            .first()
        )
        if res:
            return download_kobo_data(res)
        else:
            return jsonify({"error": "Resource not found"}), 404

    @blueprint.route("/api/2/kobo-info/<token>/<uid>/<url>", methods=["GET"])
    def get_asset_info(token, uid, url):
        headers = {"Authorization": "Token {}".format(token)}
        base_url = "https://{}/api/v2/assets/{}.json".format(url, uid)
        response = req.get(base_url, headers=headers)
        if response.status_code == 200:
            return jsonify(response.json())
        return jsonify({"error": "Resource not found"}), 404
