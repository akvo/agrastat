import ckan.plugins.toolkit as toolkit

impact_area_list = [
    "Production",
    "Nutrition",
    "Markets and Trade",
    "Seed systems",
    "Sustainable farming",
    "Policy",
]


def create_impact_areas():
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    try:
        data = {"id": "impact_areas"}
        toolkit.get_action("vocabulary_show")(context, data)
    except toolkit.ObjectNotFound:
        data = {"name": "impact_areas"}
        vocab = toolkit.get_action("vocabulary_create")(context, data)
        for tag in impact_area_list:
            data = {"name": tag, "vocabulary_id": vocab["id"]}
            toolkit.get_action("tag_create")(context, data)
