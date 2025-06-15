Explication du code source
==========================

Cette section décrit en détail les deux parties fondamentales du projet **Smart Waste Detection**,
qui repose sur l'utilisation de deux modèles YOLOv8 (You Only Look Once version 8) combinés dans une architecture innovante :

1. Le **modèle de détection binaire** : détermine si un objet constitue un déchet ou non selon le contexte
2. Le **modèle de classification multi-classe** : identifie le type de déchet parmi 5 catégories principales

Cette approche en pipeline permet d'optimiser les performances et la précision du système de reconnaissance.

------------------------------------------------------------
1. Détection binaire : Objet est-il un déchet ?
------------------------------------------------------------

Le premier modèle constitue la **porte d'entrée** du système. Il est entraîné pour **détecter la présence d'un déchet dans une image** en tenant compte du contexte environnemental. Il ne classe pas le type de déchet, mais détermine si l'objet observé est considéré comme un **déchet** ou **non-déchet**.

**Code d'implémentation :**

.. code-block:: python

   from ultralytics import YOLO
   import cv2
   import numpy as np

   # Chargement du modèle de détection binaire
   model_detect = YOLO("/content/drive/MyDrive/yolov8_best_smartdetection.pt")

   # Prédiction sur une image
   results = model_detect("image.jpg")

   # Filtrage des objets identifiés comme déchets avec seuil de confiance
   confidence_threshold = 0.5
   waste_boxes = [
       box for box in results[0].boxes 
       if box.cls == 0 and box.conf >= confidence_threshold
   ]

   print(f"Nombre de déchets détectés : {len(waste_boxes)}")

**Caractéristiques techniques :**

- **Architecture** : YOLOv8n (version nano pour rapidité d'exécution)
- **Classes d'entraînement** : 2 classes (`waste` et `non_waste`)
- **Fichier modèle** : `yolov8_best_smartdetection.pt`
- **Détection contextuelle** : Analyse l'environnement pour la classification
- **Seuil de confiance** : Filtrage des détections peu fiables

**Avantages de cette approche :**

- **Pré-filtrage efficace** : Réduit les faux positifs avant classification
- **Performance optimisée** : Évite le traitement d'objets non pertinents
- **Contextualisation** : Prend en compte la situation de l'objet
- **Rapidité d'exécution** : Modèle léger pour traitement temps réel

------------------------------------------------------------
2. Classification multi-classe : Quel type de déchet ?
------------------------------------------------------------

Le deuxième modèle est **spécialisé** pour classifier les objets qui ont été identifiés comme déchets lors de l'étape précédente. Cette segmentation permet d'obtenir une classification plus précise et ciblée.

**Code d'implémentation :**

.. code-block:: python

   # Chargement du modèle de classification multi-classe
   model_classify = YOLO("/content/drive/MyDrive/yolov8_best.pt")

   def crop_image(image_path, bbox):
       """
       Fonction pour recadrer l'image selon les coordonnées de la bounding box
       
       Args:
           image_path (str): Chemin vers l'image source
           bbox (tensor): Coordonnées [x1, y1, x2, y2] de la bounding box
           
       Returns:
           numpy.ndarray: Image recadrée
       """
       image = cv2.imread(image_path)
       x1, y1, x2, y2 = map(int, bbox)
       cropped = image[y1:y2, x1:x2]
       return cropped

   # Traitement de chaque objet identifié comme déchet
   for i, box in enumerate(waste_boxes):
       # Extraction (recadrage) de la région d'intérêt
       cropped_img = crop_image("image.jpg", box.xyxy[0])
       
       # Classification de l'objet recadré
       classification_result = model_classify(cropped_img)
       
       # Extraction des résultats
       predicted_class = classification_result[0].probs.top1
       confidence = classification_result[0].probs.top1conf.item()
       class_name = classification_result[0].names[predicted_class]
       
       print(f"Déchet {i+1}: {class_name} (confiance: {confidence:.2f})")

**Classes gérées par le modèle de classification :**

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - ID
     - Type de déchet
     - Description et exemples
   * - 0
     - Plastique
     - Bouteilles, emballages, sacs plastiques, contenants
   * - 1
     - Verre
     - Bouteilles en verre, pots, contenants transparents  
   * - 2
     - Métal
     - Canettes, emballages métalliques, capsules
   * - 3
     - Papier
     - Feuilles, journaux, documents, magazines
   * - 4
     - Carton
     - Boîtes, emballages cartonnés, cartons ondulés

------------------------------------------------------------
3. Pipeline complet intégré
------------------------------------------------------------

Voici l'implémentation complète du pipeline combinant détection binaire et classification multi-classe :

.. code-block:: python

   from ultralytics import YOLO
   import cv2
   import numpy as np
   from typing import List, Tuple, Dict

   class SmartWasteDetector:
       """
       Système de détection et classification intelligente des déchets
       """
       
       def __init__(self, detection_model_path: str, classification_model_path: str):
           """
           Initialisation des modèles
           
           Args:
               detection_model_path (str): Chemin vers le modèle de détection
               classification_model_path (str): Chemin vers le modèle de classification
           """
           self.model_detect = YOLO(detection_model_path)
           self.model_classify = YOLO(classification_model_path)
           
           # Classes de déchets
           self.waste_classes = {
               0: "Plastique",
               1: "Verre", 
               2: "Métal",
               3: "Papier",
               4: "Carton"
           }
       
       def crop_image(self, image: np.ndarray, bbox: List[float]) -> np.ndarray:
           """Recadrage de l'image selon la bounding box"""
           x1, y1, x2, y2 = map(int, bbox)
           return image[y1:y2, x1:x2]
       
       def process_image(self, image_path: str, confidence_threshold: float = 0.5) -> List[Dict]:
           """
           Traitement complet d'une image
           
           Args:
               image_path (str): Chemin vers l'image à analyser
               confidence_threshold (float): Seuil de confiance minimum
               
           Returns:
               List[Dict]: Liste des déchets détectés avec leurs caractéristiques
           """
           # Chargement de l'image
           image = cv2.imread(image_path)
           
           # Étape 1: Détection binaire
           detection_results = self.model_detect(image)
           
           waste_detections = []
           
           # Filtrage des objets détectés comme déchets
           for box in detection_results[0].boxes:
               if box.cls == 0 and box.conf >= confidence_threshold:
                   # Étape 2: Recadrage de l'objet
                   cropped_img = self.crop_image(image, box.xyxy[0])
                   
                   # Étape 3: Classification du type de déchet
                   classification_result = self.model_classify(cropped_img)
                   
                   # Extraction des informations
                   predicted_class = classification_result[0].probs.top1
                   class_confidence = classification_result[0].probs.top1conf.item()
                   
                   waste_info = {
                       'bbox': box.xyxy[0].tolist(),
                       'detection_confidence': box.conf.item(),
                       'waste_type': self.waste_classes[predicted_class],
                       'classification_confidence': class_confidence,
                       'coordinates': {
                           'x1': int(box.xyxy[0][0]),
                           'y1': int(box.xyxy[0][1]),
                           'x2': int(box.xyxy[0][2]),
                           'y2': int(box.xyxy[0][3])
                       }
                   }
                   
                   waste_detections.append(waste_info)
           
           return waste_detections

   # Utilisation du système complet
   detector = SmartWasteDetector(
       detection_model_path="/content/drive/MyDrive/yolov8_best_smartdetection.pt",
       classification_model_path="/content/drive/MyDrive/yolov8_best.pt"
   )

   # Analyse d'une image
   results = detector.process_image("test_image.jpg", confidence_threshold=0.6)

   # Affichage des résultats
   for i, waste in enumerate(results):
       print(f"Déchet {i+1}:")
       print(f"  Type: {waste['waste_type']}")
       print(f"  Confiance détection: {waste['detection_confidence']:.2f}")
       print(f"  Confiance classification: {waste['classification_confidence']:.2f}")
       print(f"  Position: ({waste['coordinates']['x1']}, {waste['coordinates']['y1']}) -> ({waste['coordinates']['x2']}, {waste['coordinates']['y2']})")
       print("-" * 50)

------------------------------------------------------------
4. Optimisations et bonnes pratiques
------------------------------------------------------------

**Gestion des performances :**

.. code-block:: python

   # Configuration pour optimisation GPU
   import torch
   
   # Vérification de la disponibilité CUDA
   device = 'cuda' if torch.cuda.is_available() else 'cpu'
   print(f"Dispositif utilisé: {device}")
   
   # Optimisation mémoire pour traitement par lots
   def process_batch(image_paths: List[str], batch_size: int = 4):
       """Traitement par lots pour optimiser les performances"""
       results = []
       for i in range(0, len(image_paths), batch_size):
           batch = image_paths[i:i + batch_size]
           batch_results = [detector.process_image(img) for img in batch]
           results.extend(batch_results)
       return results

**Gestion des erreurs :**

.. code-block:: python

   import logging

   def safe_process_image(self, image_path: str) -> List[Dict]:
       """Version sécurisée du traitement d'image avec gestion d'erreurs"""
       try:
           if not os.path.exists(image_path):
               raise FileNotFoundError(f"Image non trouvée: {image_path}")
           
           results = self.process_image(image_path)
           logging.info(f"Traitement réussi: {len(results)} déchets détectés")
           return results
           
       except Exception as e:
           logging.error(f"Erreur lors du traitement de {image_path}: {str(e)}")
           return []

------------------------------------------------------------
5. Déploiement et intégration
------------------------------------------------------------

**Interface Streamlit :**

.. code-block:: python

   import streamlit as st
   
   st.title("🗑️ Smart Waste Detection")
   
   uploaded_file = st.file_uploader("Choisir une image", type=['jpg', 'jpeg', 'png'])
   
   if uploaded_file is not None:
       # Traitement de l'image
       results = detector.process_image(uploaded_file)
       
       # Affichage des résultats
       if results:
           st.success(f"{len(results)} déchet(s) détecté(s)")
           for waste in results:
               st.write(f"**{waste['waste_type']}** - Confiance: {waste['classification_confidence']:.2f}")
       else:
           st.info("Aucun déchet détecté dans l'image")

**API REST avec FastAPI :**

.. code-block:: python

   from fastapi import FastAPI, File, UploadFile
   from fastapi.responses import JSONResponse
   
   app = FastAPI(title="Smart Waste Detection API")
   detector = SmartWasteDetector("model1.pt", "model2.pt")
   
   @app.post("/detect-waste/")
   async def detect_waste(file: UploadFile = File(...)):
       """Endpoint pour la détection de déchets"""
       try:
           # Sauvegarde temporaire du fichier
           temp_path = f"temp_{file.filename}"
           with open(temp_path, "wb") as buffer:
               buffer.write(await file.read())
           
           # Traitement
           results = detector.process_image(temp_path)
           
           # Nettoyage
           os.remove(temp_path)
           
           return JSONResponse({
               "status": "success",
               "detections": len(results),
               "results": results
           })
           
       except Exception as e:
           return JSONResponse({
               "status": "error", 
               "message": str(e)
           }, status_code=500)

------------------------------------------------------------
6. Métriques et évaluation
------------------------------------------------------------

**Calcul des métriques de performance :**

.. code-block:: python

   def evaluate_model_performance(test_images: List[str], ground_truth: List[Dict]) -> Dict:
       """
       Évaluation des performances du modèle
       
       Returns:
           Dict: Métriques de performance (précision, rappel, F1-score)
       """
       true_positives = 0
       false_positives = 0
       false_negatives = 0
       
       for i, image_path in enumerate(test_images):
           predictions = detector.process_image(image_path)
           ground_truth_labels = ground_truth[i]
           
           # Calcul des métriques (simplifié)
           # Implementation détaillée selon vos critères d'évaluation
           
       precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
       recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
       f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
       
       return {
           'precision': precision,
           'recall': recall, 
           'f1_score': f1_score
       }

------------------------------------------------------------
7. Remarques techniques et optimisations
------------------------------------------------------------

**Considérations importantes :**

- **Préprocessing** : Normalisation des images pour cohérence des résultats
- **Post-processing** : Filtrage des détections selon seuils de confiance
- **Gestion mémoire** : Libération des ressources après traitement
- **Batch processing** : Traitement par lots pour optimiser les performances
- **Cache des modèles** : Éviter le rechargement répétitif des modèles

**Optimisations avancées :**

.. code-block:: python

   # Optimisation pour production
   class OptimizedWasteDetector(SmartWasteDetector):
       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           # Préchargement et optimisation des modèles
           self.model_detect.export(format='onnx')  # Export ONNX pour rapidité
           
       def preprocess_image(self, image: np.ndarray) -> np.ndarray:
           """Préprocessing standardisé des images"""
           # Redimensionnement, normalisation, etc.
           return cv2.resize(image, (640, 640))

------------------------------------------------------------
8. Tests et validation
------------------------------------------------------------

**Suite de tests unitaires :**

.. code-block:: python

   import unittest
   
   class TestSmartWasteDetector(unittest.TestCase):
       
       def setUp(self):
           self.detector = SmartWasteDetector("model1.pt", "model2.pt")
       
       def test_image_processing(self):
           """Test du traitement d'image basique"""
           results = self.detector.process_image("test_image.jpg")
           self.assertIsInstance(results, list)
       
       def test_crop_functionality(self):
           """Test de la fonction de recadrage"""
           image = np.zeros((100, 100, 3), dtype=np.uint8)
           cropped = self.detector.crop_image(image, [10, 10, 50, 50])
           self.assertEqual(cropped.shape, (40, 40, 3))

------------------------------------------------------------
9. Conclusion technique
------------------------------------------------------------

L'architecture proposée offre plusieurs **avantages significatifs** :

**Performance et précision :**
- **Réduction des faux positifs** grâce au pré-filtrage binaire
- **Classification spécialisée** pour une meilleure précision typologique  
- **Traitement optimisé** avec pipeline séquentiel efficace

**Flexibilité et évolutivité :**
- **Modèles indépendants** permettant l'amélioration séparée
- **Architecture modulaire** facilitant l'intégration
- **Déploiement adaptatif** (local, cloud, edge computing)

**Applications pratiques :**
- **Temps réel** : Caméras de surveillance environnementale
- **Traitement par lots** : Analyse de grandes quantités d'images
- **Interface utilisateur** : Applications web et mobile
- **API REST** : Intégration dans systèmes existants

Cette approche **dual-model** constitue une solution robuste et scalable pour la détection intelligente des déchets, ouvrant la voie vers des applications industrielles et environnementales concrètes.

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
