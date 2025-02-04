import ckan.plugins.toolkit as toolkit

value_chain_list = [
    "Beans",
    "Soya Beans",
    "Avocado",
    "Chili",
    "Poutry",
    "Maize",
    "Wheat",
]


def create_value_chains():
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    try:
        data = {"id": "value_chains"}
        toolkit.get_action("vocabulary_show")(context, data)
    except toolkit.ObjectNotFound:
        data = {"name": "value_chains"}
        vocab = toolkit.get_action("vocabulary_create")(context, data)
        for tag in value_chain_list:
            data = {"name": tag, "vocabulary_id": vocab["id"]}
            toolkit.get_action("tag_create")(context, data)
