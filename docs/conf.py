# Configuration Sphinx - conf.py
import os
import sys

# Configuration du projet
project = 'Smart Waste Detection'
copyright = '2025, Votre Nom'
author = 'Votre Nom'
release = '1.0.0'

# Extensions Sphinx
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'recommonmark',
]

# Configuration des templates
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Configuration du thème
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Personnalisation
html_title = "Smart Waste Detection - Documentation"
html_short_title = "Smart Waste Detection"
html_logo = "_static/logo.png"  # Ajoutez votre logo
html_favicon = "_static/favicon.ico"  # Ajoutez votre favicon

# Fichiers statiques
html_static_path = ['_static']

# Configuration des liens
html_context = {
    "display_github": True,
    "github_user": "votre-username",
    "github_repo": "smart-waste-detection",
    "github_version": "main",
    "conf_py_path": "/docs/",
}
html_theme = 'furo'
html_theme_options = {
    "source_repository": "https://github.com/votre-username/smart-waste-detection/",
    "source_branch": "main",
    "source_directory": "docs/",
}
