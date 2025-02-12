import ckan.plugins.toolkit as toolkit
from flask import Blueprint, request
import requests


def page_external(blueprint):
    @blueprint.route("/faostat")
    def faostat_page():
        page = request.args.get("page", "")
        return toolkit.render("faostat.html", {"page": page})
