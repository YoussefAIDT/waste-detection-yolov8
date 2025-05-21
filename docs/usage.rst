Utilisation du modèle
=====================

1. Ouvrir le notebook `yolov8_waste_detect.ipynb` sur Google Colab.
2. Installer les bibliothèques nécessaires :
   ``pip install ultralytics opencv-python matplotlib``
3. Télécharger le modèle `yolov8_best.pt` et le placer ici :
   ``/content/drive/MyDrive/yolov8_best.pt``

4. Charger le modèle :
   .. code-block:: python

      from ultralytics import YOLO
      model = YOLO("/content/drive/MyDrive/yolov8_best.pt")

5. Tester avec une image `image_test.jpg`
6. Afficher le résultat de prédiction
