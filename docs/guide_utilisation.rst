Guide d'utilisation
===================

Ce projet permet de détecter automatiquement différents types de **déchets** dans des **images** ou **vidéos** à l'aide de modèles **YOLOv8 pré-entraînés**, combinant détection intelligente et classification avancée.

Structure du projet
-------------------

Le projet comprend **trois notebooks principaux** :

* ``Smart_waste_detection.ipynb`` : modèle qui détecte si un objet est un **déchet ou non**
* ``yolov8_waste_detect.ipynb`` : modèle de **classification** des types de déchets  
* ``Application_de_computer_vision.ipynb`` : application complète combinant détection + classification, avec **interface Streamlit**

.. note::
   Le fichier ``Application_de_computer_vision.ipynb`` est le notebook principal recommandé pour une utilisation complète du système.

Guide complet d'installation et d'utilisation
---------------------------------------------

Configuration avec Google Colab + Streamlit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Ouvrir le projet sur Google Colab**
   
   Accédez au dossier ``Models``, puis ouvrez le fichier ``Application_de_computer_vision.ipynb``.

   .. raw:: html

      <a href="https://colab.research.google.com/github/zakariazemmahi/waste-detection-yolov8/blob/main/Models/Application_de_comptur_vision.ipynb#scrollTo=ZgGV1in-5PaZ" 
         target="_blank" 
         rel="noopener noreferrer"
         onclick="window.open(this.href, '_blank'); return false;">
        <img src="https://colab.research.google.com/assets/colab-badge.svg" 
             alt="Ouvrir dans Colab" 
             style="height: 40px;">
      </a>

2. **Télécharger et importer les modèles pré-entraînés**
   
   Récupérez les deux modèles depuis le dossier ``ModelsSauvegarde`` :
   
   * ``yolov8_best.pt`` → classification du type de déchet (5 catégories)
   * ``yolov8_best_smartdetection.pt`` → détection déchet ou non-déchet
   
   Placez-les dans votre Google Drive et ajustez les chemins dans le code :

   .. code-block:: python

      model_detect = "/content/drive/MyDrive/yolov8_best_smartdetection.pt"
      model_classify = "/content/drive/MyDrive/yolov8_best.pt"

   .. tip::
      Activez l'exécution GPU dans Colab (Runtime → Change runtime type → GPU) pour des performances optimales.

   .. important::
      **Placement des modèles :** Assurez-vous que les deux modèles sont placés dans le même répertoire de votre Google Drive pour garantir le bon fonctionnement de l'application.

3. **Installer les dépendances**
   
   Dans le notebook ``Application_de_computer_vision.ipynb``, exécutez séquentiellement les cellules pour :
   
   * Monter Google Drive
   * Installer les bibliothèques nécessaires (ultralytics, streamlit, etc.)
   * Générer automatiquement le fichier ``app.py``

4. **Lancer l'application web Streamlit via LocalTunnel**
   
   a. Obtenez votre adresse IP publique :

   .. code-block:: bash

      !wget -q -O - ipv4.icanhazip.com

   b. Copiez l'adresse IP affichée, puis lancez l'application :

   .. code-block:: bash

      !streamlit run app.py & npx localtunnel --port 8501

   c. Une URL similaire à ``https://floppy-tools-retire.loca.lt`` apparaîtra. Cliquez dessus.
   
   d. Collez l'adresse IP copiée dans le champ "Tunnel Password" et cliquez sur "Click to Submit".

5. **Utilisation de l'interface web**
   
   L'interface Streamlit offre une expérience utilisateur intuitive :
   
   * **Upload d'image** : Glissez-déposez ou sélectionnez une image
   * **Détection automatique** : Le système analyse l'image en temps réel
   * **Classification intelligente** : Si un déchet est détecté, il est automatiquement classé
   * **Résultats visuels** : Affichage des boîtes de détection avec labels et scores de confiance

Fonctionnalités avancées
------------------------

Architecture du système
~~~~~~~~~~~~~~~~~~~~~~~~

Le système utilise une approche en deux étapes :

1. **Détection primaire** : YOLOv8 détermine si l'objet est un déchet
2. **Classification secondaire** : Si c'est un déchet, classification en 5 catégories

Types de déchets reconnus
~~~~~~~~~~~~~~~~~~~~~~~~~

* 🥤 **Plastique** : Bouteilles, contenants, sacs
* 🍷 **Verre** : Bouteilles, bocaux (incluant porcelaine/céramique)  
* 🥫 **Métal** : Canettes, boîtes de conserve
* 📄 **Papier** : Documents, journaux
* 📦 **Carton** : Boîtes, emballages

Performance et optimisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Temps de traitement** : < 2 secondes par image
* **Précision** : > 85% sur les tests de validation
* **Formats supportés** : JPG, PNG, JPEG
* **Taille max** : 10 MB par image

Remarques importantes et dépannage
----------------------------------

Configuration recommandée
~~~~~~~~~~~~~~~~~~~~~~~~~

* **Runtime Colab** : GPU activé (obligatoire pour de bonnes performances)
* **Connexion internet** : Stable (nécessaire pour LocalTunnel)
* **Navigateur** : Chrome ou Firefox recommandés

Problèmes courants et solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problème** : L'URL LocalTunnel ne fonctionne pas
   **Solution** : Réexécutez la cellule de lancement Streamlit

**Problème** : Erreur de chargement des modèles
   **Solution** : Vérifiez les chemins vers les fichiers .pt dans Google Drive

**Problème** : Performances lentes
   **Solution** : Activez le GPU dans les paramètres de runtime Colab

**Problème** : Session expirée
   **Solution** : La session Colab doit rester active. Relancez si nécessaire.

Limitations
~~~~~~~~~~~

* La session Colab doit rester active pendant toute l'utilisation
* Le lien LocalTunnel peut expirer après inactivité
* Traitement limité aux images statiques (pas de vidéo en temps réel)

Contact et Support
==================

Équipe de développement
----------------------

Pour toute question, suggestion ou problème technique, contactez l'équipe :

**Étudiants développeurs :**

* **Youssef ES-SAAIDI** 
  
  * GitHub: `@YoussefAIDT <https://github.com/YoussefAIDT>`_
  * Email: youssef.essaaidi@ensam-meknes.ma

* **Zakariae ZEMMAHI**
  
  * GitHub: `@zakariazemmahi <https://github.com/zakariazemmahi>`_
  * Email: zakariae.zemmahi@ensam-meknes.ma

* **Mohamed HAJJI**
  
  * GitHub: `@mohamedhajji11 <https://github.com/mohamedhajji11>`_
  * Email: mohamed.hajji@ensam-meknes.ma

**Encadrant académique :**

* **Pr. Tawfik MASROUR**
  
  * Email: tawfik.masrour@ensam-meknes.ma
  * Département: Intelligence Artificielle et Technologies de Data

Support technique
-----------------

Types de support disponibles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Issues GitHub** : Signalement de bugs et demandes d'amélioration
* **Documentation** : Guide complet et FAQ disponibles
* **Support académique** : Assistance pour l'utilisation dans le cadre pédagogique

Comment obtenir de l'aide
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Consultez d'abord la documentation** et les sections de dépannage
2. **Vérifiez les issues existantes** sur le repository GitHub
3. **Créez une nouvelle issue** avec :
   
   * Description détaillée du problème
   * Étapes pour reproduire l'erreur
   * Captures d'écran si applicable
   * Informations sur votre environnement

4. **Contactez l'équipe** directement pour les questions urgentes

Contribution au projet
----------------------

Le projet est ouvert aux contributions ! Pour participer :

1. Forkez le repository
2. Créez une branche pour votre fonctionnalité
3. Effectuez vos modifications
4. Soumettez une Pull Request

**Types de contributions recherchées :**

* Amélioration de la précision des modèles
* Optimisation des performances
* Ajout de nouveaux types de déchets
* Amélioration de l'interface utilisateur
* Documentation et traductions

Institution
-----------

**École Nationale Supérieure d'Arts et Métiers (ENSAM)**

* **Adresse** : Meknès, Maroc
* **Site web** : `www.ensam-meknes.ma <http://www.ensam-meknes.ma>`_
* **Département** : Génie Intelligence Artificielle et Technologies de Data - Systèmes Industriels

.. note::
   Ce projet s'inscrit dans le cadre des activités de recherche et développement de l'ENSAM Meknès, contribuant à l'innovation dans le domaine de l'intelligence artificielle appliquée à l'environnement.
