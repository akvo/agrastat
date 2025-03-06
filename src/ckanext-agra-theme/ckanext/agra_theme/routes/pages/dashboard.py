import ckan.plugins.toolkit as toolkit


def page_dashboard(blueprint):
    @blueprint.route("/poc/dashboard")
    def dashboard():
        return toolkit.render("dashboard/index.html", {})
