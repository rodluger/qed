# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import qed
import sys
import os
from examples import run_examples

# Hacks
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
on_rtd = os.environ.get("READTHEDOCS") == "True"


# -- Project information -----------------------------------------------------

project = "qed"
copyright = "2021, Rodrigo Luger"
author = "Rodrigo Luger"
version = qed.__version__
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
]

# If we're on READTHEDOCS, `rtds_action` will run the examples for us!
if on_rtd:
    extensions += ["rtds_action"]
else:
    run_examples()

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_options = {"display_version": True}
html_last_updated_fmt = "%Y %b %d at %H:%M:%S UTC"
html_show_sourcelink = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".


# -- rtds_action settings -----------------------------------------------------

rtds_action_github_repo = "rodluger/qed"
rtds_action_path = "examples"
rtds_action_artifact_prefix = "examples-for-"
rtds_action_github_token = os.environ.get("GITHUB_TOKEN", "")
