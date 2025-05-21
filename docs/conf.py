# Configuration de la documentation Sphinx pour Read the Docs

import os
import sys

# Ajouter le dossier parent au chemin système
sys.path.insert(0, os.path.abspath('..'))

# Informations sur le projet
project = 'Waste Detection YOLOv8'
author = 'Zakariae Zemmahi/ES-SAAIDI Youssef/HAJJI Mohamed'
:release = '1.0'

# Extensions utilisées par Sphinx
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo'
]

# Chemins vers les templates
templates_path = ['_templates']

# Fichiers à exclure
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Thème HTML
html_theme = 'sphinx_rtd_theme'

# Fichiers statiques (CSS personnalisé, images, etc.)
html_static_path = ['_static']

# Ajouter un fichier CSS personnalisé
html_css_files = [
    'custom_readthedocs_css.css'
]

# Options de thème (optionnel)
html_theme_options = {
    'navigation_depth': 3,
    'collapse_navigation': False,
    'sticky_navigation': True,
}

# Logo personnalisé (optionnel)
# html_logo = '_static/logo.png'

# Favicon (optionnel)
# html_favicon = '_static/favicon.ico'
