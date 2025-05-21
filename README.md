# Détection de déchets avec YOLOv8

Ce projet permet de détecter différents types de déchets à partir d'images et de vidéos en utilisant un modèle YOLOv8 pré-entraîné.

## Guide d'installation et d'utilisation

### Étape 1 : Ouvrir le projet dans Google Colab

1. Téléchargez le fichier notebook `yolov8_waste_detect.ipynb`
2. Ouvrez Google Colab (https://colab.research.google.com/)
3. Importez le notebook en cliquant sur "Fichier" > "Importer un notebook"
4. Sélectionnez le fichier `yolov8_waste_detect.ipynb`

### Étape 2 : Installation des bibliothèques nécessaires

Exécutez les cellules d'installation dans le notebook pour installer toutes les dépendances requises.

### Étape 3 : Téléchargement des données du projet

Suivez les instructions dans le notebook pour télécharger les données nécessaires.

### Étape 4 : Intégration du modèle pré-entraîné

1. Accédez à GitHub pour télécharger le fichier de modèle `yolov8_best.pt`
2. Connectez votre Google Drive à Colab
3. Placez le modèle dans votre Google Drive en respectant le chemin suivant :
   `/content/drive/MyDrive/yolov8_best.pt`

### Étape 5 : Chargement du modèle

Exécutez la cellule suivante dans le notebook :

```python
from ultralytics import YOLO
# Charger le modèle entraîné
model = YOLO("/content/drive/MyDrive/yolov8_best.pt")
```

### Étape 6 : Test du modèle

1. Téléchargez une image de test contenant des déchets et nommez-la `image_test.jpg`
2. Exécutez la cellule de prédiction pour analyser l'image
3. Visualisez les résultats de détection

Vous pouvez également tester le modèle sur des vidéos en suivant les instructions du notebook.

### Étape 7 : Lancement de l'application Streamlit

1. Installez les bibliothèques requises pour Streamlit
2. Exécutez toutes les cellules restantes du notebook
3. Dans la cellule finale, exécutez :
   ```
   !streamlit run app.py & npx localtunnel --port 8501
   ```
4. Une URL sera générée

### Étape 8 : Accès à l'interface web

1. Exécutez la commande suivante pour obtenir votre adresse IP :
   ```
   !wget -q -O - ipv4.icanhazip.com
   ```
2. Copiez l'adresse IP affichée
3. Dans la page qui s'ouvre après avoir cliqué sur l'URL générée, collez l'adresse IP dans le champ "Tunnel Password"
4. Cliquez sur "Click to submit"
5. Vous accéderez à l'interface web de l'application de détection de déchets

## Fonctionnalités

- Détection de différents types de déchets sur des images
- Analyse de vidéos pour la détection de déchets
- Interface utilisateur web intuitive via Streamlit

## Remarques

Assurez-vous que votre session Colab reste active pendant l'utilisation de l'application Streamlit.
