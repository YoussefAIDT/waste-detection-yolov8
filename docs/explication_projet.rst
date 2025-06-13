Explication générale du projet
==============================

Ce projet de vision par ordinateur a pour but de **détecter automatiquement les déchets** dans des images et de **classer ces déchets** selon leur type. Il utilise deux modèles YOLOv8 entraînés indépendamment : 

1. Un modèle pour savoir **si un objet est un déchet ou non**
2. Un second pour **classer le type de déchet détecté**

Collecte et préparation des données
-----------------------------------

Nous avons collecté manuellement des images dans notre école, en utilisant un téléphone portable. Ces photos représentent différentes situations (déchets ou objets non jetés).

.. note::

   Ci-dessous quelques exemples d'images capturées :

   .. image:: ../images/photo_table_bouteille.jpg
      :alt: Bouteille sur une table - non déchet
      :width: 300px

   .. image:: photo_main_bouteille.jpg.png
      :alt: Bouteille dans la main - non déchet
      :width: 300px

   .. image:: ../images/photo_sol_bouteille.jpg
      :alt: Bouteille au sol - déchet
      :width: 300px

Toutes les images ont été **annotées (labelisées)** via **Roboflow**, une plateforme d’étiquetage d'images en ligne. Nous avons ensuite **divisé les images** en trois parties : entraînement, validation et test.

.. image:: ../images/roboflow_capture.png
   :alt: Capture d'écran Roboflow
   :width: 600px

Modèle 1 – Détection Déchet ou Non-Déchet
------------------------------------------

Ce modèle est entraîné pour distinguer si un objet est **un déchet ou non**, en se basant sur **le contexte de la scène**. Quelques exemples illustratifs :

- Une **bouteille sur une table** → *non déchet*
- Une **bouteille tenue dans la main** → *non déchet*
- Une **bouteille jetée au sol** → *déchet*
- Un **papier dans une poubelle** → *non déchet*
- Un **papier jeté par terre** → *déchet*

.. image:: ../images/bouteille_table.jpg
   :alt: Bouteille sur table
   :width: 250px

.. image:: ../images/bouteille_main.jpg
   :alt: Bouteille dans la main
   :width: 250px

.. image:: ../images/bouteille_sol.jpg
   :alt: Bouteille jetée au sol
   :width: 250px

Modèle 2 – Classification des types de déchets
----------------------------------------------

Une fois qu'un objet est détecté comme **déchet**, il est ensuite classé parmi **5 types** courants rencontrés à l'école :

1. Plastique
2. Carton
3. Papier
4. Verre (Glass)
5. Métal

Voici des exemples de chaque classe :

.. image:: ../images/plastique_exemple.jpg
   :alt: Déchet plastique
   :width: 200px

.. image:: ../images/carton_exemple.jpg
   :alt: Déchet carton
   :width: 200px

.. image:: ../images/papier_exemple.jpg
   :alt: Déchet papier
   :width: 200px

.. image:: ../images/glass_exemple.jpg
   :alt: Déchet verre
   :width: 200px

.. image:: ../images/metal_exemple.jpg
   :alt: Déchet métal
   :width: 200px

Conclusion
----------

Cette double approche (détection + classification) permet d'obtenir un système **intelligent**, capable de **reconnaître les déchets** et de **les catégoriser** automatiquement, afin d’**aider à la propreté et au tri sélectif** dans les écoles et espaces publics.

