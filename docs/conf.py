from pickle import TRUE
import sphinx_rtd_theme

# General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx_rtd_theme', 'sphinx.ext.autodoc', 'sphinx.ext.todo', 'sphinx.ext.autosummary']
autodoc_member_order = 'bysource'
todo_include_todos = True

templates_path = ['_templates']
source_suffix = '.rst'

master_doc = 'contents'

project = "AGRASTAT"
copyright = "2024, Akvo"
author = "Akvo"
html_show_sphinx = False

epub_show_urls = "footnote"
exclude_patterns = ["Thumbs.db", ".DS_Store"]
html_theme = "sphinx_rtd_theme"


def setup(app):
    app.add_css_file("css/custom.css")



html_css_files = [
    "css/custom.css",
]
html_static_path = ["_static"]
html_theme_options = {
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    # Toc options
    "collapse_navigation": TRUE,
    "sticky_navigation": True,
    "navigation_depth": -1,
    "includehidden": TRUE,
    "titles_only": False,
}
htmlhelp_basename = 'AGRASTATdoc'
