import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Smart Waste Detection'
copyright = '2025, Ayoub Zemmahi'
author = 'Zakariae Zemmahi / ES-SAAIDI Youssef / HAJJI Mohamed'
release = '1.0'

extensions = ['recommonmark', 'sphinx.ext.autodoc', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
