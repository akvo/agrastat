import requests
import ckan.plugins.toolkit as toolkit

country_list = [
    "Malawi",
    "Zambia",
    "Ghana",
    "Senegal",
    "Rwanda",
    "Kenya",
    "Uganda",
    "Mali",
    "Cote d Ivoire",
    "Mozambique",
    "Nigeria",
    "Ethiopia",
    "Tanzania",
    "Burkina Faso",
    "Togo",
]


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
            data = {"name": tag, "vocabulary_id": vocab["id"]}
            toolkit.get_action("tag_create")(context, data)
