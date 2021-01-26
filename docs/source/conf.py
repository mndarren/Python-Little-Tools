# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import python_little_tools
import sphinx_rtd_theme

_pysrc = os.path.abspath(os.path.join(os.path.abspath(__file__), '', '', ''))
sys.path.insert(0, _pysrc)

# -- Project information -----------------------------------------------------

project = 'python_little_tools'
copyright = '2021, Darren Xie'
author = 'Darren Xie'


# To allow __init__() to be documented automatically
def skip(app, what, name, obj, skip, options):
    if name == "__init__":
        return False
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.todo',
              'sphinx.ext.viewcode',
              'rst2pdf.pdfbuilder',
              ]
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
version = python_little_tools.__version__
release = python_little_tools.__release__

# List of patterns, relative to source1 directory, that match files and
# directories to ignore when looking for source1 files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_sidebars = {
    '**': [
        'relations.html',
        'searchbox.html'
    ]
}
htmlhelp_basename = 'python_little_tools_doc'

# PDF Document for rst2pdf
pdf_documents = [
    ('index', u'python_little_tools', u'Python Little Tools Documentation', u'Darrne Xie')
]
