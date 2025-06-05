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
