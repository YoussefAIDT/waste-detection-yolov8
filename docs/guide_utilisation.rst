Guide d'utilisation
===================

Ce projet permet de détecter automatiquement différents types de déchets dans des images ou vidéos à l'aide de modèles YOLOv8 pré-entraînés, combinant détection intelligente et classification.

Structure du projet
-------------------

Le projet comprend trois notebooks principaux :

- ``Smart_waste_detection.ipynb`` : modèle qui détecte si un objet est un déchet ou non.
- ``yolov8_waste_detect.ipynb`` : modèle de classification des types de déchets.
- ``Application_de_computer_vision.ipynb`` : application complète combinant détection + classification, avec interface Streamlit.

Guide d'installation et d'utilisation (Google Colab + Streamlit)
-----------------------------------------------------------------

1. **Ouvrir le projet sur Google Colab**

   Accédez au dossier ``Models``, puis ouvrez le fichier ``Application_de_computer_vision.ipynb``. Cliquez sur *Open in Colab*.

2. **Télécharger et importer les modèles pré-entraînés**

   Récupérez les deux modèles depuis le dossier ``ModelsSauvegarde`` :

   - ``yolov8_best.pt`` → classification du type de déchet
   - ``yolov8_best_smartdetection.pt`` → détection déchet ou non

   Placez-les dans votre Google Drive. Utilisez les chemins suivants dans le notebook :

   ::

      model_detect = "/content/drive/MyDrive/yolov8_best_smartdetection.pt"
      model_classify = "/content/drive/MyDrive/yolov8_best.pt"

   .. note::

      ✅ Astuce : activez l'exécution GPU dans Colab pour de meilleures performances.

3. **Installer les dépendances**

   Dans le notebook ``Application_de_computer_vision.ipynb`` :

   - Montez Google Drive
   - Installez les bibliothèques nécessaires : ``ultralytics``, ``streamlit``, etc.
   - Générez le fichier ``app.py`` avec le code de l'application

4. **Lancer l'application web Streamlit via LocalTunnel**

   Exécutez la cellule suivante pour récupérer l'adresse IP publique :

   ::

      !wget -q -O - ipv4.icanhazip.com

   Puis lancez Streamlit avec tunnel public :

   ::

      !streamlit run app.py & npx localtunnel --port 8501

   Une URL de type ``https://xxxxx.loca.lt`` s’affichera. Cliquez dessus pour accéder à l’application.

5. **Utilisation de l’interface web**

   - Chargez une ou plusieurs images
   - L’application détecte les objets
   - Si un objet détecté est un déchet, il sera classifié (plastique, verre, papier, métal, carton)
   - Sinon, l'application indiquera que ce n'est pas un déchet

Fonctionnalités
---------------

- Détection intelligente de déchets sur images et vidéos
- Classification automatique en 5 types
- Interface web Streamlit intégrée à Google Colab via LocalTunnel
- Aucune installation locale requise

Remarques importantes
---------------------

- La session Google Colab doit rester active pendant toute l’utilisation
- Si l'URL LocalTunnel expire, relancez la cellule correspondante
- L'utilisation du GPU est fortement recommandée
