# ♻️ Détection intelligente de déchets avec YOLOv8

Ce projet permet de détecter automatiquement différents types de **déchets** dans des **images** ou **vidéos** à l'aide de modèles **YOLOv8 pré-entraînés**, combinant détection intelligente et classification.

---

## 📁 Structure du projet

Le projet comprend **trois notebooks principaux** :
- `Smart_waste_detection.ipynb` : modèle qui détecte si un objet est un **déchet ou non**
- `yolov8_waste_detect.ipynb` : modèle de **classification** des types de déchets
- `Application_de_computer_vision.ipynb` : application complète combinant détection + classification, avec **interface Streamlit**

---

## ⚙️ Guide complet d'installation et d'utilisation (Google Colab + Streamlit)

### 1. **Ouvrir le projet sur Google Colab**
Accédez au dossier `Models`, puis ouvrez le fichier `Application_de_computer_vision.ipynb`. Cliquez sur **"Open in Colab"**.

### 2. **Télécharger et importer les modèles pré-entraînés**
Récupérez les deux modèles depuis le dossier `ModelsSauvegarde` :
- `yolov8_best.pt` → classification du type de déchet
- `yolov8_best_smartdetection.pt` → détection déchet ou non

Placez-les dans votre Google Drive. Assurez-vous d'utiliser les bons chemins dans le notebook :
```python
model_detect = "/content/drive/MyDrive/yolov8_best_smartdetection.pt"
model_classify = "/content/drive/MyDrive/yolov8_best.pt"
```

**✅ Astuce :** Activez l'exécution GPU dans Colab pour de meilleures performances.

### 3. **Installer les dépendances**
Toujours dans le notebook `Application_de_computer_vision.ipynb`, exécutez les premières cellules pour :
- Monter Google Drive
- Installer les bibliothèques nécessaires (ultralytics, streamlit, etc.)
- Générer le fichier `app.py` avec le code de l'application

### 4. **Lancer l'application web Streamlit via LocalTunnel**
Exécutez cette cellule pour récupérer votre adresse IP publique :
```bash
!wget -q -O - ipv4.icanhazip.com
```
Copiez l'adresse IP affichée (ex : `34.16.147.252`)

Puis lancez Streamlit avec tunnel public :
```bash
!streamlit run app.py & npx localtunnel --port 8501
```
Une URL comme `https://loose-spoons-report.loca.lt` s'affichera. Cliquez dessus pour accéder à l'interface web.

### 5. **Utilisation de l'interface web**
Une fois dans l'application :
- Chargez une ou plusieurs images
- L'application détectera les objets
- Si l'objet détecté est un déchet, il sera classifié par type (plastique, verre, papier, métal, carton)
- Sinon, le système indique que ce n'est pas un déchet

---

## ✅ Fonctionnalités

- Détection intelligente de déchets sur images et vidéos
- Classification automatique en 5 types de déchets
- Interface web conviviale avec Streamlit intégrée à Google Colab via LocalTunnel
- Aucune installation locale nécessaire

---

## ⚠️ Remarques importantes

- La session Colab doit rester active pendant toute l'utilisation
- Le lien généré par LocalTunnel peut expirer : il suffit de réexécuter la cellule pour obtenir un nouveau lien
- L'utilisation du GPU est fortement conseillée pour une meilleure rapidité de traitement
