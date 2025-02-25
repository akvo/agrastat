import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
from .routes.api.kobo import api_kobo
from .cli import kobo as kobo_cli

kobo_blueprint = Blueprint("kobo", __name__)

api_kobo(kobo_blueprint)


class KoboPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IClick)

    # IClick
    def get_commands(self):
        return [kobo_cli]

    # IBlueprint
    def get_blueprint(self):
        return kobo_blueprint

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("fanstatic", "kobo")
