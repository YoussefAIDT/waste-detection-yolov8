import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Waste Detection YOLOv8'
author = 'Zakariae Zemmahi / ES-SAAIDI Youssef / HAJJI Mohamed'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom_readthedocs_css.css']

html_theme_options = {
    'navigation_depth': 3,
    'collapse_navigation': False,
    'sticky_navigation': True,
}
