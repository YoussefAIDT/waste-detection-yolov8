Détection intelligente de déchets avec YOLOv8
=============================================

Ce projet permet de détecter automatiquement différents types de **déchets** dans des **images** ou **vidéos** à l'aide de modèles **YOLOv8 pré-entraînés**, combinant détection intelligente et classification.

Structure du projet
-------------------

Le projet comprend **trois notebooks principaux** :

- ``Smart_waste_detection.ipynb`` : modèle qui détecte si un objet est un **déchet ou non**
- ``yolov8_waste_detect.ipynb`` : modèle de **classification** des types de déchets
- ``Application_de_computer_vision.ipynb`` : application complète combinant détection + classification, avec **interface Streamlit**

Guide complet d'installation et d'utilisation (Google Colab + Streamlit)
-------------------------------------------------------------------------

1. **Ouvrir le projet sur Google Colab**

Accédez au dossier ``Models``, puis ouvrez le fichier ``Application_de_computer_vision.ipynb``. Cliquez sur **"Open in Colab"**.

2. **Télécharger et importer les modèles pré-entraînés**

Récupérez les deux modèles depuis le dossier ``ModelsSauvegarde`` :

- ``yolov8_best.pt`` → classification du type de déchet
- ``yolov8_best_smartdetection.pt`` → détection déchet ou non

Placez-les dans votre Google Drive. Exemple de chemins à utiliser :

.. code-block:: python

   model_detect = "/content/drive/MyDrive/yolov8_best_smartdetection.pt"
   model_classify = "/content/drive/MyDrive/yolov8_best.pt"

**Astuce :** Activez l'exécution GPU dans Colab pour de meilleures performances.

3. **Installer les dépendances**

Dans le notebook ``Application_de_computer_vision.ipynb``, exécutez les premières cellules pour :

- Monter Google Drive
- Installer les bibliothèques nécessaires (ultralytics, streamlit…)
- Générer le fichier ``app.py``

4. **Lancer l'application web Streamlit via LocalTunnel**

.. code-block:: bash

   !wget -q -O - ipv4.icanhazip.com

Copiez l'adresse IP affichée, puis :

.. code-block:: bash

   !streamlit run app.py & npx localtunnel --port 8501

Une URL comme ``https://loose-spoons-report.loca.lt`` apparaîtra. Cliquez dessus pour accéder à l'application.

5. **Utilisation de l'interface web**

- Chargez une image
- Le système détecte et classe les déchets automatiquement

Fonctionnalités
---------------

- Détection intelligente de déchets (images/vidéos)
- Classification en 5 types : plastique, verre, métal, papier, carton
- Interface web Streamlit + Google Colab
- Sans installation locale

Remarques importantes
---------------------

- Colab doit rester actif
- Lien LocalTunnel peut expirer (rechargez)
- Utilisez le **GPU** pour de meilleures performances
