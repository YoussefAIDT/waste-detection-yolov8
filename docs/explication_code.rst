
Explication du code source
==========================

Cette section décrit en détail les deux parties fondamentales du projet Smart Waste Detection,
qui repose sur l’utilisation de deux modèles YOLOv8 combinés :

1. Le **modèle de détection binaire** : détecte si un objet est un déchet ou non.
2. Le **modèle de classification** : détermine le type de déchet parmi 5 classes.

------------------------------------------------------------
1. Détection : Objet est-il un déchet ?
------------------------------------------------------------

Le premier modèle est entraîné pour **détecter la présence d’un déchet dans une image**. Il ne classe pas le type,
mais indique si l’objet est considéré comme un **déchet** ou **non**.

.. code-block:: python

   from ultralytics import YOLO

   # Chargement du modèle de détection binaire
   model_detect = YOLO("/content/drive/MyDrive/yolov8_best_smartdetection.pt")

   # Prédiction sur une image
   results = model_detect("image.jpg")

   # Filtrage des objets identifiés comme déchets
   waste_boxes = [box for box in results[0].boxes if box.cls == 0]

**Détails importants :**

- Le modèle a été entraîné avec YOLOv8 sur un dataset personnalisé contenant deux classes : `waste` et `non_waste`.
- Ce modèle est léger (YOLOv8n) pour une exécution rapide.
- Le fichier du modèle est nommé `yolov8_best_smartdetection.pt`.

**Objectif** : filtrer uniquement les objets pertinents avant de les transmettre au modèle de classification.

------------------------------------------------------------
2. Classification : Quel type de déchet ?
------------------------------------------------------------

Le deuxième modèle est spécialisé pour classer les objets qui ont été détectés comme déchets à l’étape précédente.

.. code-block:: python

   # Chargement du modèle de classification multi-classe
   model_classify = YOLO("/content/drive/MyDrive/yolov8_best.pt")

   # Pour chaque objet identifié comme déchet, effectuer la classification
   for box in waste_boxes:
       # Extraction (recadrage) de l’objet
       cropped_img = crop_image("image.jpg", box.xyxy)

       # Classification de l’objet recadré
       result = model_classify(cropped_img)

       # Affichage des résultats
       print(result[0].names[result[0].probs.top1])

**Classes gérées par le modèle** :

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - ID
     - Type de déchet
   * - 0
     - Plastique
   * - 1
     - Verre
   * - 2
     - Métal
   * - 3
     - Papier
   * - 4
     - Carton

------------------------------------------------------------
3. Intégration des deux modèles dans un pipeline
------------------------------------------------------------

Voici un aperçu du pipeline complet combinant détection binaire puis classification :

.. code-block:: python

   from ultralytics import YOLO

   model_detect = YOLO("/content/drive/MyDrive/yolov8_best_smartdetection.pt")
   model_classify = YOLO("/content/drive/MyDrive/yolov8_best.pt")

   results = model_detect("image.jpg")
   for box in results[0].boxes:
       if box.cls == 0:  # 0 = classe "déchet"
           cropped = crop_image("image.jpg", box.xyxy)
           classification = model_classify(cropped)
           print("Type de déchet :", classification[0].names[classification[0].probs.top1])

------------------------------------------------------------
4. Remarques techniques
------------------------------------------------------------

- Le recadrage `crop_image` doit être défini pour extraire la zone de l’image contenant le déchet.
- YOLOv8 accepte les images sous forme de chemin de fichier ou de tableau NumPy.
- Chaque modèle a été entraîné indépendamment avec Roboflow et Ultralytics.

------------------------------------------------------------
5. Conclusion
------------------------------------------------------------

L’utilisation combinée de ces deux modèles permet :
- Une détection plus fiable (réduction des faux positifs)
- Une classification plus précise et ciblée
- Une architecture flexible pouvant être déployée sur divers environnements (Colab, caméra, interface Streamlit)

