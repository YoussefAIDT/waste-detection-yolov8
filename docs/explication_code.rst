
Explication du code source
==========================

Cette section détaille le fonctionnement du code Python utilisé pour entraîner et utiliser le modèle Smart Waste Detection basé sur YOLOv8.

Installation des dépendances
----------------------------

Les bibliothèques suivantes sont installées via `pip` :

.. code-block:: python

   !pip install ultralytics
   !pip install roboflow

- `ultralytics` : bibliothèque officielle pour utiliser YOLOv8.
- `roboflow` : utilisée pour importer facilement un dataset annoté depuis la plateforme Roboflow.

Chargement du dataset
---------------------

Le dataset annoté est téléchargé depuis Roboflow :

.. code-block:: python

   from roboflow import Roboflow
   rf = Roboflow(api_key="VOTRE_CLE_API")
   project = rf.workspace("nom_workspace").project("nom_du_projet")
   version = project.version(1)
   dataset = version.download("yolov8")

Le jeu de données est directement structuré au format YOLOv8 (fichiers `.yaml`, `images/`, `labels/`).

Montage de Google Drive
------------------------

Pour stocker les modèles et y accéder depuis Colab :

.. code-block:: python

   from google.colab import drive
   drive.mount('/content/drive')

Cela permet de sauvegarder le modèle entraîné dans Google Drive et d'y accéder ensuite depuis une autre session.

Entraînement du modèle
----------------------

On utilise la commande YOLOv8 suivante pour l'entraînement :

.. code-block:: python

   !yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=50 imgsz=640

- `task=detect` : détection d'objet.
- `model=yolov8n.pt` : on utilise ici la version "nano" du modèle YOLOv8 pour plus de rapidité.
- `data=data.yaml` : fichier YAML généré automatiquement par Roboflow contenant les chemins vers les images et les classes.
- `epochs=50` : nombre d'itérations d'entraînement.
- `imgsz=640` : taille des images redimensionnées.

Évaluation du modèle
--------------------

Une fois l'entraînement terminé, YOLO affiche les performances du modèle (mAP, précision, rappel).

.. code-block:: python

   !yolo task=detect mode=val model=/content/runs/detect/train/weights/best.pt data=data.yaml

Détection sur des images personnalisées
---------------------------------------

Le modèle est ensuite utilisé pour prédire des déchets sur des images :

.. code-block:: python

   !yolo task=detect mode=predict model=/content/drive/MyDrive/yolov8_best.pt source="image.jpg"

Cela génère une image avec les boîtes englobantes autour des objets détectés.
