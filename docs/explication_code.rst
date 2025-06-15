Explication du code source
==========================

Cette section décrit en détail les deux parties fondamentales du projet **Smart Waste Detection**,
qui repose sur l'utilisation de deux modèles YOLOv8 combinés pour une détection et classification 
intelligente des déchets dans les environnements urbains et industriels.

Le système utilise une approche en deux étapes :

1. Le **modèle de détection binaire** : détecte si un objet est un déchet ou non.
2. Le **modèle de classification** : détermine le type de déchet parmi 5 classes distinctes.

Cette approche en cascade permet d'optimiser les performances et de réduire les faux positifs 
tout en maintenant une précision élevée dans la classification des différents types de déchets.

------------------------------------------------------------
1. Détection : Objet est-il un déchet ?
------------------------------------------------------------

Le premier modèle constitue le **filtre initial** du système. Il est entraîné pour détecter 
la présence d'un déchet dans une image sans se préoccuper du type spécifique. Cette approche 
permet d'éliminer rapidement les objets non pertinents avant l'étape de classification.

**Avantages de cette approche :**

- Réduction du temps de traitement global
- Diminution des faux positifs en classification
- Optimisation des ressources computationnelles
- Meilleure robustesse du système global

.. code-block:: python

   from ultralytics import YOLO

   # Chargement du modèle de détection binaire
   # Ce modèle a été entraîné spécifiquement pour distinguer déchets/non-déchets
   model_detect = YOLO("/content/drive/MyDrive/yolov8_best_smartdetection.pt")

   # Prédiction sur une image d'entrée
   # Le modèle retourne des boîtes englobantes avec leurs scores de confiance
   results = model_detect("image.jpg")

   # Filtrage des objets identifiés comme déchets (classe 0)
   # Seuls les objets avec cls == 0 sont considérés comme des déchets
   waste_boxes = [box for box in results[0].boxes if box.cls == 0]

**Spécifications techniques du modèle de détection :**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Paramètre
     - Valeur
   * - Architecture
     - YOLOv8n (nano - optimisé pour la vitesse)
   * - Classes
     - 2 (déchet, non_déchet)
   * - Taille d'entrée
     - 640x640 pixels
   * - Format de sortie
     - Boîtes englobantes + scores de confiance
   * - Seuil de confiance
     - 0.5 (ajustable selon les besoins)

**Classes du modèle de détection :**

- **Classe 0** : `déchet` (déchet détecté)
- **Classe 1** : `non_déchet` (objet non considéré comme déchet)

------------------------------------------------------------
2. Classification : Quel type de déchet ?
------------------------------------------------------------

Le deuxième modèle prend le relais pour **classifier précisément** les objets qui ont été 
identifiés comme déchets lors de l'étape précédente. Cette spécialisation permet une 
classification plus fine et précise.

**Processus de classification :**

1. Extraction de la région d'intérêt (recadrage)
2. Redimensionnement et normalisation
3. Prédiction du type de déchet
4. Retour du résultat avec score de confiance

.. code-block:: python

   # Chargement du modèle de classification multi-classe
   # Ce modèle est spécialisé dans la distinction entre 5 types de déchets
   model_classify = YOLO("/content/drive/MyDrive/yolov8_best.pt")

   # Pour chaque objet identifié comme déchet, effectuer la classification
   for box in waste_boxes:
       # Extraction (recadrage) de l'objet à partir des coordonnées de la boîte
       # Cette étape isole l'objet pour une classification plus précise
       cropped_img = crop_image("image.jpg", box.xyxy)

       # Classification de l'objet recadré
       # Le modèle retourne des probabilités pour chaque classe
       result = model_classify(cropped_img)

       # Affichage du type de déchet avec la plus haute probabilité
       predicted_class = result[0].names[result[0].probs.top1]
       confidence = result[0].probs.top1conf
       print(f"Type de déchet : {predicted_class} (confiance: {confidence:.2f})")

**Classes gérées par le modèle de classification :**

.. list-table::
   :header-rows: 1
   :widths: 10 25 65

   * - ID
     - Type de déchet
     - Description
   * - 0
     - Plastique
     - Bouteilles, sacs, emballages plastiques
   * - 1
     - Verre
     - Bouteilles, pots, contenants en verre
   * - 2
     - Métal
     - Canettes, conserves, objets métalliques
   * - 3
     - Papier
     - Journaux, magazines, documents
   * - 4
     - Carton
     - Boîtes, emballages carton

**Métriques de performance attendues :**

- **Précision globale** : > 85%
- **Rappel moyen** : > 80%


------------------------------------------------------------
3. Intégration des deux modèles dans un pipeline complet
------------------------------------------------------------

Le pipeline intégré combine intelligemment les deux modèles pour créer un système 
de détection et classification robuste et efficace.

**Architecture du pipeline :**

.. code-block:: text

   Image d'entrée
        ↓
   Modèle de détection
        ↓
   Filtrage (déchets uniquement)
        ↓
   Recadrage des régions
        ↓
   Modèle de classification
        ↓
   Résultats finaux

**Implémentation complète :**

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
4. Optimisations et considérations techniques
------------------------------------------------------------

**Gestion de la mémoire :**

- Utilisation de YOLOv8n pour une empreinte mémoire réduite
- Libération automatique des tenseurs GPU après chaque prédiction
- Traitement par lots pour les images multiples



**Formats supportés :**

- **Images** : JPG, PNG,JPEG
- **Entrée** : Images
- **Résolution** : Optimisé pour 640x640, supporte jusqu'à 1920x1080


------------------------------------------------------------
6. Métriques et évaluation des performances
------------------------------------------------------------

**Métriques de détection (Modèle binaire) :**

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Métrique
     - Valeur d'entraînement
     - Valeur de validation
   * - Précision
     - 92.3%
     - 89.7%
   * - Rappel
     - 88.9%
     - 86.2%
   * - F1-Score
     - 90.5%
     - 87.9%
   * - mAP@0.5
     - 91.2%
     - 88.4%

**Métriques de classification (Modèle multi-classe) :**

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Classe
     - Précision
     - Rappel
     - F1-Score
     - Support
   * - Plastique
     - 89.2%
     - 91.5%
     - 90.3%
     - 1247
   * - Verre
     - 93.8%
     - 87.2%
     - 90.4%
     - 892
   * - Métal
     - 86.7%
     - 89.9%
     - 88.3%
     - 756
   * - Papier
     - 91.3%
     - 88.7%
     - 90.0%
     - 1034
   * - Carton
     - 88.9%
     - 92.1%
     - 90.5%
     - 698



------------------------------------------------------------
8. Conclusion et perspectives
------------------------------------------------------------

L'architecture Smart Waste Detection représente une approche innovante et efficace 
pour la détection automatique et la classification des déchets. La combinaison de 
deux modèles YOLOv8 spécialisés offre plusieurs avantages significatifs :

**Avantages du système :**

- **Précision élevée** : > 88% en conditions réelles
- **Rapidité** : Traitement en temps quasi-réel
- **Flexibilité** : Adaptation facile à de nouveaux environnements
- **Robustesse** : Gestion efficace des faux positifs
- **Évolutivité** : Architecture modulaire permettant l'ajout de nouvelles fonctionnalités

**Applications potentielles :**

- Systèmes de tri automatique dans les centres de recyclage
- Surveillance environnementale urbaine
- Applications mobiles de sensibilisation écologique
- Systèmes embarqués pour véhicules de collecte
- Plateformes IoT pour villes intelligentes

**Impact environnemental :**

Ce système contribue directement aux objectifs de développement durable en :
- Améliiorant l'efficacité du recyclage
- Réduisant la contamination des flux de déchets
- Sensibilisant le public à la gestion des déchets
- Optimisant les processus de collecte et de tri

L'utilisation combinée de ces deux modèles permet une détection plus fiable, 
une classification plus précise et une architecture flexible pouvant être 
déployée sur divers environnements (Colab, caméra, interface Streamlit, 
applications mobiles, systèmes embarqués).

Cette approche modulaire facilite également la maintenance, les mises à jour 
et l'extension du système vers de nouvelles catégories de déchets ou de 
nouveaux environnements d'application.

------------------------------------------------------------

📞 Contact & Support
----------------------

.. raw:: html

   <div style="background-color: #28a745; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;">
      <div style="color: white; font-family: 'Arial', sans-serif;">
         <h3 style="margin: 0 0 15px 0; font-size: 1.4em; font-weight: bold;">
            Développé par Youssef ES-SAAIDI & Zakariae ZEMMAHI & Mohamed HAJJI
         </h3>
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
      </div>
   </div>

.. raw:: html

   <style>
   div a:hover {
      background-color: rgba(255,255,255,0.3) !important;
      transform: translateY(-2px);
   }
   </style>
