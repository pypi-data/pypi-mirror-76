# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import subprocess
import configparser
import os
from alveolus import settings
# sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------
subprocess.call('doxygen doxygen.conf', shell=True)

if os.path.isfile(os.path.join(settings.WORKING_DIR, 'alveolus-config.ini')):
    config_file = os.path.join(settings.WORKING_DIR, 'alveolus-config.ini')
else:
    config_file = os.path.join(settings.SOURCE_DIR, 'alveolus-config.ini')

main_conf_parser = configparser.RawConfigParser()
main_conf_parser.optionxform = str
main_conf_parser.read(config_file)

project = main_conf_parser['PROJECT']['name']
copyright = main_conf_parser['PROJECT']['copyright']
author = main_conf_parser['PROJECT']['author']

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["breathe", "exhale"]

# -- Breathe and Exhale Configuration -----------------------------------------


breathe_projects = {
     project: main_conf_parser['CONFIG_DIRECTORIES']['output']+"/doxygen/xml"
}
breathe_default_project = project
exhale_args = {
    # These arguments are required
    "containmentFolder": os.path.join(main_conf_parser['CONFIG_DIRECTORIES']['src_api'], 'doxygen_src'),
    "rootFileName": "library_root.rst",
    "rootFileTitle": "Library API",
    "doxygenStripFromPath": "..",
    # Suggested optional arguments
    "createTreeView": False,
    # TIP: if using the sphinx-bootstrap-theme, you need
    # "treeViewIsBootstrap": True,
    "exhaleExecutesDoxygen": False,
    # "exhaleDoxygenStdin": "INPUT = @DOC_BUILD_DIR@/doxygen/xml"
}

# -- Syntax Configuration -----------------------------------------
primary_domain = 'cpp'
highlight_language = 'cpp'
source_suffix = {
    '.rst': 'restructuredtext',
}
source_encoding = 'UTF-8'
# -- Directory Configuration -----------------------------------------
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'output', 'cmake', '.idea']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = main_conf_parser['STYLE']['sphinx_theme']
