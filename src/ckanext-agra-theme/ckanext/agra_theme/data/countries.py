import requests
import ckan.plugins.toolkit as toolkit

countries_data = requests.get(
    "https://gist.githubusercontent.com/almost/7748738/raw/575f851d945e2a9e6859fb2308e95a3697bea115/countries.json"
).json()
country_list = [{"name": c["name"], "value": c["code"]} for c in countries_data]


def create_countries():
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    try:
        data = {"id": "countries"}
        toolkit.get_action("vocabulary_show")(context, data)
    except toolkit.ObjectNotFound:
        data = {"name": "countries"}
        vocab = toolkit.get_action("vocabulary_create")(context, data)
        for tag in country_list:
            data = {"name": tag["value"], "vocabulary_id": vocab["id"]}
            toolkit.get_action("tag_create")(context, data)
