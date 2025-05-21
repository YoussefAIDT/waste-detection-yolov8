# 🚮 Détection de déchets avec YOLOv8 + Streamlit (Google Colab)

Ce projet permet de détecter automatiquement les déchets (plastique, verre, métal, papier, carton) à partir d’images ou de vidéos, en utilisant **YOLOv8**. Il inclut une application Web interactive avec **Streamlit**.

---

## ✅ Étapes d'utilisation

### 1. Accéder au projet dans Google Colab

- Ouvrir le fichier `yolov8_waste_detect.ipynb` dans ce dépôt.
- Ou cliquer directement ici pour lancer dans Colab :  
  [![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/<TON_UTILISATEUR_GITHUB>/waste-detection-yolov8/blob/main/yolov8_waste_detect.ipynb)

---

### 2. Installer les bibliothèques nécessaires

Dans Colab, exécuter les cellules suivantes pour installer les dépendances :

```bash
pip install ultralytics opencv-python matplotlib streamlit localtunnel
3. Télécharger le modèle YOLOv8 entraîné
Aller sur GitHub et télécharger le fichier yolov8_best.pt.

Le placer dans ton Google Drive à cet emplacement exact :

bash
Copier
Modifier
/content/drive/MyDrive/yolov8_best.pt
4. Charger le modèle
Tu n’as pas besoin de réentraîner le modèle. Il suffit d’exécuter cette cellule :

python
Copier
Modifier
from ultralytics import YOLO

# Charger ton modèle entraîné
model = YOLO("/content/drive/MyDrive/yolov8_best.pt")
5. Tester une image
Télécharge une image contenant un déchet et nomme-la :

Copier
Modifier
image_test.jpg
Exécute la cellule de prédiction dans le notebook pour afficher les résultats.

6. Tester une vidéo (optionnel)
Une cellule dans le notebook permet également de tester le modèle sur une vidéo.

7. Lancer l’application Web (Streamlit)
Les bibliothèques nécessaires doivent être déjà installées.

Exécute toutes les cellules restantes dans le notebook.

Lance la commande suivante dans une cellule :

bash
Copier
Modifier
!streamlit run app.py & npx localtunnel --port 8501
Une ligne affichera un code :

bash
Copier
Modifier
!wget -q -O - ipv4.icanhazip.com
Copie le code retourné par cette commande et colle-le dans :

yaml
Copier
Modifier
Tunnel Password:
Clique sur Click to Submit

Tu accèderas à l'application Streamlit depuis un lien généré
