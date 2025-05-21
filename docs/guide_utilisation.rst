Guide d'installation et d'utilisation
=====================================

Ce guide explique comment exécuter le projet de détection de déchets avec YOLOv8 dans Google Colab, tester des images ou vidéos, et accéder à l'interface Web Streamlit.

Étape 1 : Ouvrir le projet dans Google Colab
--------------------------------------------

1. Accédez au fichier ``yolov8_waste_detect.ipynb`` dans le dépôt GitHub.
2. Cliquez sur le bouton **Open in Colab** (ou ouvrez ce lien dans Colab).
3. Vous pouvez également télécharger le fichier ``yolov8_waste_detect.ipynb``.
4. Rendez-vous sur https://colab.research.google.com/
5. Cliquez sur **Fichier > Importer un notebook**
6. Sélectionnez le fichier téléchargé.

Étape 2 : Installation des bibliothèques nécessaires
-----------------------------------------------------

Exécutez les cellules d'installation dans le notebook pour installer toutes les dépendances :

.. code-block:: bash

   pip install ultralytics opencv-python matplotlib streamlit localtunnel

Étape 3 : Téléchargement des données
-------------------------------------

Les instructions pour télécharger les données du projet (via Roboflow ou un autre lien) sont disponibles directement dans le notebook.

Étape 4 : Intégration du modèle pré-entraîné
--------------------------------------------

1. Téléchargez le modèle ``yolov8_best.pt`` depuis le dépôt GitHub ou un lien fourni.
2. Connectez votre Google Drive à Colab.
3. Placez le fichier dans ce chemin exact :

::

   /content/drive/MyDrive/yolov8_best.pt

Étape 5 : Chargement du modèle
-------------------------------

Dans le notebook, exécutez la cellule suivante :

.. code-block:: python

   from ultralytics import YOLO

   # Charger le modèle entraîné
   model = YOLO("/content/drive/MyDrive/yolov8_best.pt")

Étape 6 : Test du modèle
-------------------------

1. Téléchargez une image contenant des déchets, nommez-la ``image_test.jpg``.
2. Chargez-la dans Colab.
3. Utilisez la cellule de prédiction pour obtenir les résultats.

Il est aussi possible d’analyser des **vidéos** en suivant les instructions du notebook.

Étape 7 : Lancement de l’application Streamlit
-----------------------------------------------

1. Assurez-vous que les bibliothèques Streamlit et LocalTunnel sont installées.
2. Exécutez toutes les cellules du notebook.
3. Lancez la commande suivante :

.. code-block:: bash

   !streamlit run app.py & npx localtunnel --port 8501

4. Une URL d’accès sera générée.

Étape 8 : Accès à l’interface Web
----------------------------------

1. Exécutez la commande suivante pour obtenir votre adresse IP :

.. code-block:: bash

   !wget -q -O - ipv4.icanhazip.com

2. Copiez l’adresse affichée.
3. Collez-la dans le champ **Tunnel Password** de la page générée.
4. Cliquez sur **Click to Submit**.
5. L’interface Streamlit s’ouvrira dans une nouvelle page.

Fonctionnalités
===============

- Détection de déchets sur des images (plastique, métal, verre, papier, carton)
- Analyse de vidéos
- Interface Web dynamique via Streamlit

Remarques
=========

Assurez-vous que la session Colab reste **active et non expirée** pendant l’utilisation de l’application Web.

