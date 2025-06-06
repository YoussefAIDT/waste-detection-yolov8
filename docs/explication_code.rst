Description des fichiers sources
================================

1. Smart_waste_detection.ipynb – Détection Déchet / Non-Déchet
--------------------------------------------------------------

Ce notebook utilise un modèle YOLOv8 personnalisé entraîné pour détecter si un objet est un **déchet ou non**.

**Étapes principales du code** :

- Installation des bibliothèques nécessaires :
  .. code-block:: python

     !pip install ultralytics roboflow

- Connexion à Roboflow pour charger le dataset annoté :
  .. code-block:: python

     from roboflow import Roboflow
     rf = Roboflow(api_key="...")
     project = rf.workspace("...").project("waste-detection")
     dataset = project.version(1).download("yolov8")

- Montage de Google Drive pour sauvegarder les modèles :
  .. code-block:: python

     from google.colab import drive
     drive.mount('/content/drive')

- Entraînement d’un modèle YOLOv8 :
  .. code-block:: python

     !yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=50 imgsz=640

Ce modèle est sauvegardé sous le nom : `yolov8_best_smartdetection.pt`. Il détecte **la présence d’un déchet**, sans se soucier du type.

---

2. yolov8_waste_detect.ipynb – Classification du type de déchet
----------------------------------------------------------------

Ce second notebook utilise un autre modèle YOLOv8, **entraîné uniquement sur les objets identifiés comme déchets**. Il permet de déterminer la classe du déchet :

- Plastique
- Verre
- Métal
- Papier
- Carton

**Étapes clés** :

- Chargement du dataset annoté via Roboflow
- Préparation du fichier `data.yaml` (classes et chemins)
- Entraînement d’un modèle YOLOv8 pour la classification multi-classes
  .. code-block:: python

     !yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=60 imgsz=640

Ce modèle est sauvegardé comme `yolov8_best.pt` et il est utilisé **seulement après qu’un objet ait été détecté comme déchet.**

---

Utilisation combinée des deux modèles
=====================================

L'application finale combine les deux modèles :

.. code-block:: python

   model_detect = YOLO("/content/drive/MyDrive/yolov8_best_smartdetection.pt")
   model_classify = YOLO("/content/drive/MyDrive/yolov8_best.pt")

1. **Détection globale** : `model_detect` localise les objets et indique s’ils sont des déchets.
2. **Classification ciblée** : `model_classify` détermine le type exact de chaque déchet détecté.

Cette stratégie séquentielle permet de filtrer les objets non pertinents et de garantir une classification fiable.

