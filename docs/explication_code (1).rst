
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



Modèle Smart Waste Detection
============================

Le modèle **Smart Waste Detection** est basé sur **YOLOv8**, un algorithme de détection d’objets en temps réel de dernière génération. Ce modèle a été entraîné spécifiquement pour reconnaître cinq types de déchets dans des environnements variés (sol, rue, sol de cantine, etc.).

Objectif
--------

L’objectif est double :

1. **Détecter automatiquement** les objets qui sont des déchets dans une image.
2. **Classer** ces déchets selon leur type : plastique, métal, papier, carton, ou verre.

Architecture utilisée
---------------------

Le modèle est basé sur **YOLOv8n** (version "nano"), pour optimiser la vitesse et l’utilisation des ressources :

- Architecture : CNN avec détection par ancrage.
- Entrée : Images de taille redimensionnée (640x640).
- Sortie : Boîtes englobantes avec une classe et un score de confiance.

Transfert learning
------------------

Le projet utilise le **transfert learning**. Cela signifie que :

- Le modèle YOLOv8 pré-entraîné sur le dataset COCO a été réutilisé.
- Une fine-tuning a été appliquée à partir de ce modèle sur un dataset annoté manuellement via **Roboflow**.

Classes détectées
-----------------

Le modèle reconnaît les classes suivantes :

.. csv-table:: Classes détectées
   :header: "Classe", "ID", "Description"
   :widths: 20, 10, 60

   "Plastique", 0, "Déchets plastiques (bouteilles, sacs, etc.)"
   "Verre", 1, "Bouteilles ou fragments de verre"
   "Métal", 2, "Canettes, boîtes de conserve, etc."
   "Papier", 3, "Feuilles, journaux, papiers froissés"
   "Carton", 4, "Emballages, boîtes"

Améliorations prévues
---------------------

- Ajout de la segmentation pour mieux délimiter les formes des déchets.
- Détection contextuelle : différencier un objet usagé (déchet) d’un objet propre posé (non-déchet).
- Intégration dans un pipeline complet avec caméra en temps réel.

