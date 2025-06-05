# Configuration Sphinx
import os
import sys

# Configuration du projet
project = 'Smart Waste Detection'
copyright = '2025, Votre Nom'
author = 'Votre Nom'
release = '1.0.0'

# Extensions Sphinx - MINIMAL
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

# Configuration des fichiers
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Langue française
language = 'fr'

# Configuration du thème
html_theme = 'sphinx_rtd_theme'

# Titre et description
html_title = "Smart Waste Detection Documentation"
html_short_title = "Smart Waste Detection"

# Fichiers statiques (vide pour éviter les erreurs)
html_static_path = []

# Document principal
master_doc = 'index'

# Configuration des sources
source_suffix = '.rst'
# Fichiers statiques
html_static_path = ['_static']

# CSS personnalisé
html_css_files = [
    'custom.css',
]

# Options du thème améliorées
html_theme_options = {
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}
