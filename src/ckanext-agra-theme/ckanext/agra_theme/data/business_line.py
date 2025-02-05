import ckan.plugins.toolkit as toolkit

business_line_list = [
    "Policy and Advocacy",
    "Sustainable Farming",
    "Gender and Youth",
    "Cessa",
    "IMTF",
    "Monitoring and Evaluation",
]


def create_business_lines():
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    context = {"user": user["name"]}
    try:
        data = {"id": "business_lines"}
        toolkit.get_action("vocabulary_show")(context, data)
    except toolkit.ObjectNotFound:
        data = {"name": "business_lines"}
        vocab = toolkit.get_action("vocabulary_create")(context, data)
        for tag in business_line_list:
            data = {"name": tag, "vocabulary_id": vocab["id"]}
            toolkit.get_action("tag_create")(context, data)
