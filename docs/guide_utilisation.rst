Guide_utilisation
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

   Accédez au dossier ``Models``, puis ouvrez le fichier ``Application_de_computer_vision.ipynb``.

   .. raw:: html

   <a href="https://colab.research.google.com/github/zakariazemmahi/waste-detection-yolov8/blob/main/Models/Application_de_comptur_vision.ipynb#scrollTo=ZgGV1in-5PaZ" target="_blank" rel="noopener noreferrer">
     <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Ouvrir dans Colab" style="height: 40px;">
   </a>


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

   Exécutez cette commande pour obtenir votre adresse IP :

   .. code-block:: bash

      !wget -q -O - ipv4.icanhazip.com

   Copiez l'adresse IP affichée, puis lancez l'application avec :

   .. code-block:: bash

      !streamlit run app.py & npx localtunnel --port 8501

   Une URL comme ``https://loose-spoons-report.loca.lt`` apparaîtra. Cliquez dessus pour accéder à l'application.

5. **Utilisation de l'interface web**

   - Chargez une image
   - Le système détecte les objets
   - Si l’objet est un déchet, il est classé par type
   - Sinon, le système indique que ce n’est pas un déchet

Fonctionnalités
---------------

- Détection intelligente de déchets (images et vidéos)
- Classification automatique en 5 types : plastique, verre, métal, papier, carton
- Interface web Streamlit intégrée dans Google Colab (via LocalTunnel)
- Aucune installation locale nécessaire

Remarques importantes
---------------------

- La session Colab doit rester active pendant toute l'utilisation
- Le lien généré par LocalTunnel peut expirer : il suffit de réexécuter la commande
- L'utilisation du GPU est fortement conseillée pour de meilleures performances
