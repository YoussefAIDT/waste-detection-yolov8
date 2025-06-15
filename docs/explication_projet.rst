Explication du code source
==========================

Cette section décrit en détail les deux parties fondamentales du projet **Smart Waste Detection**,
qui repose sur l’utilisation de deux modèles **YOLOv8** combinés :

1. Le **modèle de détection binaire** : détecte si un objet est un déchet ou non.
2. Le **modèle de classification** : détermine le type de déchet parmi 5 classes.

------------------------------------------------------------
1. Détection : l'objet est-il un déchet ?
------------------------------------------------------------

Le premier modèle est entraîné pour **détecter la présence d’un déchet dans une image**.
Il ne classe pas le type, mais indique si l’objet est considéré comme un **déchet** ou **non**.

.. code-block:: python

   from ultralytics import YOLO

   # Chargement du modèle de détection binaire (déchet / non-déchet)
   model_detect = YOLO("/content/drive/MyDrive/yolov8_best_smartdetection.pt")

   # Prédiction sur une image donnée
   results = model_detect("image.jpg")

   # Filtrage des objets détectés comme "déchet" (classe 0)
   waste_boxes = [box for box in results[0].boxes if box.cls == 0]

**Détails importants :**

- Le modèle a été entraîné avec **YOLOv8** sur un dataset personnalisé contenant deux classes : `waste` et `non_waste`.
- Il s’agit d’un modèle **léger (YOLOv8n)**, optimisé pour des prédictions rapides.
- Le fichier du modèle est nommé : `yolov8_best_smartdetection.pt`.

**Objectif** : filtrer uniquement les objets pertinents avant de les transmettre au modèle de classification.

------------------------------------------------------------
2. Classification : quel type de déchet ?
------------------------------------------------------------

Le deuxième modèle est spécialisé dans la **classification des objets détectés comme déchets** à l’étape précédente.

.. code-block:: python

   # Chargement du modèle de classification multi-classe
   model_classify = YOLO("/content/drive/MyDrive/yolov8_best.pt")

   # Pour chaque objet identifié comme déchet, effectuer la classification
   for box in waste_boxes:
       # Extraction (recadrage) de l’objet à partir de ses coordonnées
       cropped_img = crop_image("image.jpg", box.xyxy)

       # Classification de l’objet recadré
       result = model_classify(cropped_img)

       # Affichage de la classe prédite
       print(result[0].names[result[0].probs.top1])

**Classes gérées par le modèle :**

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

Voici un aperçu du **pipeline complet**, combinant la détection binaire et la classification :

.. code-block:: python

   from ultralytics import YOLO

   # Chargement des deux modèles
   model_detect = YOLO("/content/drive/MyDrive/yolov8_best_smartdetection.pt")
   model_classify = YOLO("/content/drive/MyDrive/yolov8_best.pt")

   # Détection initiale
   results = model_detect("image.jpg")

   for box in results[0].boxes:
       if box.cls == 0:  # Si la classe est "déchet"
           # Recadrage de l’objet détecté
           cropped = crop_image("image.jpg", box.xyxy)

           # Classification de l’objet recadré
           classification = model_classify(cropped)

           # Affichage du type de déchet prédit
           print("Type de déchet :", classification[0].names[classification[0].probs.top1])

------------------------------------------------------------
4. Remarques techniques
------------------------------------------------------------

- La fonction `crop_image` (non fournie ici) doit permettre d’extraire la **région de l’image correspondant à l’objet détecté**.
- Le modèle YOLOv8 accepte en entrée :
  - des **chemins de fichiers image**
  - ou des **tableaux NumPy** (images en mémoire)
- Chaque modèle a été entraîné indépendamment sur **Roboflow**, puis utilisé avec la bibliothèque **Ultralytics**.

------------------------------------------------------------
5. Conclusion
------------------------------------------------------------

L’utilisation combinée des deux modèles permet :

- ✅ Une détection plus fiable (réduction des faux positifs)
- ✅ Une classification plus précise et ciblée
- ✅ Une architecture flexible, compatible avec différents environnements :
  - Google Colab
  - Caméras en temps réel
  - Interfaces Web (Streamlit)

------------------------------------------------------------
6. Support technique et environnement
------------------------------------------------------------

Pour exécuter correctement ce code, voici les éléments nécessaires :

**Bibliothèques requises :**

- `ultralytics` ≥ 8.x
- `opencv-python` (si `crop_image` utilise OpenCV)
- `numpy`
- `matplotlib` *(optionnel, pour visualisation)*

**Fichiers requis :**

- `/content/drive/MyDrive/yolov8_best_smartdetection.pt` : modèle de détection binaire
- `/content/drive/MyDrive/yolov8_best.pt` : modèle de classification
- `image.jpg` : image d’entrée à analyser
- `crop_image()` : fonction utilitaire à définir pour extraire un objet à partir de coordonnées `xyxy`

**Environnement recommandé :**

- Google Colab (GPU)
- Python ≥ 3.8
- Sauvegarde des modèles sur Google Drive pour une intégration facile

**Bonnes pratiques :**

- Tester les deux modèles séparément avant l’intégration
- Vérifier le format d’image et les dimensions attendues par YOLO
- Ajouter des messages d’erreur si `waste_boxes` est vide (aucun déchet détecté)

------------------------------------------------------------
📞 Contact & Support
----------------------

.. raw:: html

   <div style="background-color: #28a745; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;">
      <div style="color: white; font-family: 'Arial', sans-serif;">
         <h3 style="margin: 0 0 15px 0; font-size: 1.4em; font-weight: bold;">
            🌱 Développé par l'équipe Smart Waste Detection
         </h3>
         <p style="margin: 10px 0; font-size: 1.1em; opacity: 0.9;">
            Youssef ES-SAAIDI • Zakariae ZEMMAHI • Mohamed HAJJI
         </p>
         <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; margin-top: 15px;">
            <div style="display: flex; align-items: center; gap: 8px;">
               <span style="font-size: 1.2em;">🐙</span>
               <a href="https://github.com/YoussefAIDT" target="_blank" style="color: #ffffff; text-decoration: none; font-weight: 500; padding: 5px 10px; background-color: rgba(255,255,255,0.2); border-radius: 5px; transition: all 0.3s ease;">
                  YoussefAIDT GitHub
               </a>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
               <span style="font-size: 1.2em;">🐙</span>
               <a href="https://github.com/zakariazemmahi" target="_blank" style="color: #ffffff; text-decoration: none; font-weight: 500; padding: 5px 10px; background-color: rgba(255,255,255,0.2); border-radius: 5px; transition: all 0.3s ease;">
                  zakariazemmahi GitHub
               </a>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
               <span style="font-size: 1.2em;">🐙</span>
               <a href="https://github.com/mohamedhajji11" target="_blank" style="color: #ffffff; text-decoration: none; font-weight: 500; padding: 5px 10px; background-color: rgba(255,255,255,0.2); border-radius: 5px; transition: all 0.3s ease;">
                  mohamedhajji11 GitHub
               </a>
            </div>
         </div>
         <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.3);">
            <p style="margin: 5px 0; font-size: 0.9em; opacity: 0.8;">
               📧 Pour toute question technique ou collaboration
            </p>
            <p style="margin: 5px 0; font-size: 0.9em; opacity: 0.8;">
               🚀 Contribuez au projet • 🌍 Ensemble pour un avenir plus propre
            </p>
         </div>
      </div>
   </div>

.. raw:: html

   <style>
   div a:hover {
      background-color: rgba(255,255,255,0.3) !important;
      transform: translateY(-2px);
   }
   </style>
