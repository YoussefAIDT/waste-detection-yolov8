# Configuration Sphinx - conf.py
import os
import sys

# Configuration du projet
project = 'Smart Waste Detection'
copyright = '2025, Votre Nom'
author = 'Votre Nom'
release = '1.0.0'
version = '1.0'

# Extensions Sphinx (minimal)
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'recommonmark',
]

# Configuration des templates
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Langue
language = 'fr'

# Configuration du thème
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
}

# Personnalisation
html_title = "Smart Waste Detection - Documentation"
html_short_title = "Smart Waste Detection"

# Fichiers statiques (optionnel)
html_static_path = []  # Vide si pas de fichiers statiques

# Source et master doc
master_doc = 'index'
source_suffix = {
    '.rst': None,
    '.md': 'recommonmark',
}
