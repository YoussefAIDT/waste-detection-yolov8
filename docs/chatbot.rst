# Chatbot Smart Waste Detection - Documentation Technique

Cette documentation présente le **Chatbot Smart Waste Detection**, un assistant intelligent utilisant le traitement du langage naturel (NLP) pour aider les utilisateurs à localiser les points de collecte de déchets et obtenir des conseils de tri personnalisés sur le campus.

---

## 1. Architecture du Système

### 1.1 Vue d'ensemble

Le chatbot combine plusieurs technologies avancées :

- **Traitement du langage naturel** : SpaCy avec modèles français optimisés
- **Similarité sémantique** : Calcul de similarité cosinus pour la compréhension des requêtes
- **Base de données dynamique** : Stockage JSON des FAQ et localisations
- **Interface utilisateur** : Streamlit pour une expérience interactive
- **Système de cache** : Optimisation des performances avec mise en cache des embeddings

```
Utilisateur (Question)
        ↓
Normalisation du texte
        ↓
Extraction d'entités (lieux)
        ↓
Calcul de similarité sémantique
        ↓
Recherche dans FAQ/Localisations
        ↓
Génération de réponse contextualisée
        ↓
Interface utilisateur (Streamlit/Console)
```

### 1.2 Composants principaux

**WasteChatbot** : Classe principale gérant :
- Traitement des requêtes utilisateur
- Recherche de correspondances dans la FAQ
- Gestion des requêtes de localisation
- Système de suggestions intelligentes
- Journalisation des conversations

---

## 2. Fonctionnalités Techniques

### 2.1 Système de traitement NLP

```python
# Chargement du modèle NLP avec fallback intelligent
try:
    nlp = spacy.load("fr_dep_news_trf")  # Modèle transformer haute précision
except:
    nlp = spacy.load("fr_core_news_md")  # Fallback si transformer indisponible
```

**Caractéristiques** :
- Support prioritaire des modèles transformer pour une meilleure précision
- Fallback automatique vers des modèles standards
- Traitement optimisé des requêtes en français
- Extraction automatique d'entités et de contexte

### 2.2 Normalisation et synonymes

Le système intègre une normalisation intelligente du texte :

```python
synonyms = {
    "td 1": "td1",
    "amphi a": "amphi a",
    "math info": "département math_info",
    "méca": "mécanique",
    "energie": "énergétique"
}

def normalize_text(text):
    text = text.lower().strip()
    # Remplacement des synonymes
    for syn, main in synonyms.items():
        text = text.replace(syn, main)
    # Suppression des caractères spéciaux
    text = re.sub(r'[^\w\s]', '', text)
    return text
```

### 2.3 Système de similarité sémantique

**Algorithme de correspondance** :
- Utilisation de la similarité cosinus entre vecteurs de mots
- Seuil de confiance ajustable (0.72 par défaut)
- Cache des embeddings pour optimiser les performances
- Recherche dans la FAQ et les localisations

```python
def find_best_match(self, query):
    """Trouve la meilleure correspondance avec score de confiance"""
    query_vec = self.get_embedding(query)
    similarities = cosine_similarity([query_vec], faq_vectors)[0]
    best_idx = np.argmax(similarities)
    return questions[best_idx], similarities[best_idx]
```

---

## 3. Gestion des Données

### 3.1 Structure des fichiers de données

Le système utilise des fichiers JSON pour une gestion flexible des données :

**data/faq.json** :
```json
{
    "Puis-je recycler une bouteille en plastique ?": "✅ Oui, les bouteilles en plastique vont dans le bac de recyclage.",
    "Où jeter les déchets organiques ?": "🥬 Les déchets organiques vont dans le composteur du jardin.",
    "Comment trier le verre ?": "🍾 Le verre va dans les conteneurs spécialisés, retirez les bouchons."
}
```

**data/locations.json** :
```json
{
    "cafétéria": {
        "poubelle": "📍 À gauche de la sortie de la cafétéria, à côté de la fontaine.",
        "entrée": "🚪 L'entrée principale est en face du bâtiment D."
    },
    "bibliothèque": {
        "poubelle": "📍 Trois points de collecte : accueil, zone lecture, et réserve.",
        "entrée": "🚪 Entrée principale côté parking étudiant."
    }
}
```

### 3.2 Chargement dynamique des données

```python
def load_data():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Chargement avec création automatique si fichiers absents
    if faq_path.exists():
        with open(faq_path, 'r', encoding='utf-8') as f:
            faq = json.load(f)
    else:
        # Initialisation avec données par défaut
        faq = default_faq_data
        with open(faq_path, 'w', encoding='utf-8') as f:
            json.dump(faq, f, ensure_ascii=False, indent=2)
    
    return faq, locations
```

---

## 4. Interface Utilisateur

### 4.1 Interface Streamlit

**Fonctionnalités** :
- Chat interactif avec historique des conversations
- Interface responsive et intuitive
- Gestion d'état avec `st.session_state`
- Indicateurs de progression pour les recherches

```python
def run_chatbot():
    st.title("♻ Assistant Intelligent de Tri des Déchets")
    st.markdown("Posez vos questions sur le recyclage ou la localisation des poubelles")
    
    # Gestion de l'historique de conversation
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # Interface de chat avec messages persistants
    for msg in st.session_state.history:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])
```

### 4.2 Mode console

Pour les tests et le développement :

```python
if __name__ == "__main__":
    print("👋 Bonjour ! Posez-moi vos questions sur le tri des déchets.")
    chatbot = WasteChatbot()
    
    while True:
        query = input("Vous: ")
        if query.lower() in ['exit', 'quit', 'bye']:
            break
        
        response = chatbot.process_query(query)
        print(f"Assistant: {response}")
```

---

## 5. Système de Recherche Intelligent

### 5.1 Traitement des requêtes de localisation

```python
def handle_location_query(self, query):
    """Gestion améliorée des requêtes de localisation"""
    query = normalize_text(query)
    best_match = None
    best_score = 0
    
    for location in self.locations:
        # Correspondance exacte prioritaire
        if normalize_text(location) in query:
            return self.locations[location]
        
        # Similarité sémantique pour requêtes approximatives
        score = cosine_similarity(
            [self.get_embedding(location)],
            [self.get_embedding(query)]
        )[0][0]
        
        if score > best_score:
            best_score = score
            best_match = location
    
    # Retour si score suffisant (seuil : 0.65)
    if best_score > 0.65:
        return self.locations[best_match]
    
    return None
```

### 5.2 Système de suggestions

Quand la confiance est faible, le système propose des alternatives :

```python
# Suggestions si faible confiance
similar_questions = [
    q for q in questions 
    if cosine_similarity(
        [self.get_embedding(q)],
        [self.get_embedding(query)]
    )[0][0] > 0.5
][:3]

response = "🤔 Je ne suis pas sûr de comprendre. Voici des suggestions :\n"
response += "\n".join(f"• {q}" for q in similar_questions)
```

---

## 6. Optimisations et Performances

### 6.1 Système de cache

```python
def get_embedding(self, text):
    """Cache les embeddings pour améliorer les performances"""
    if text not in self.vector_cache:
        self.vector_cache[text] = nlp(text).vector
    return self.vector_cache[text]
```

### 6.2 Statistiques d'utilisation

Le chatbot collecte des métriques pour l'amélioration continue :

```python
self.stats = defaultdict(int)

# Tracking par type de requête
self.stats['location_queries'] += 1  # Requêtes de localisation
self.stats['faq_queries'] += 1       # Questions FAQ
self.stats['unknown_queries'] += 1   # Requêtes non comprises
```

### 6.3 Journalisation

```python
def log_conversation(self, query, response):
    """Journalisation des conversations"""
    self.conversation_history.append({
        'query': query,
        'response': response,
        'timestamp': datetime.now().isoformat()
    })
```

---

## 7. Installation et Configuration

### 7.1 Dépendances requises

```bash
# Installation des packages principaux
pip install spacy scikit-learn numpy streamlit

# Téléchargement des modèles français
python -m spacy download fr_core_news_md
python -m spacy download fr_dep_news_trf  # Optionnel, pour de meilleures performances
```

### 7.2 Structure des fichiers

```
projet/
├── main.py                 # Script principal
├── data/
│   ├── faq.json           # Base de données FAQ
│   └── locations.json     # Données de localisation
├── requirements.txt       # Dépendances
└── README.md             # Documentation utilisateur
```

### 7.3 Lancement de l'application

```bash
# Mode Streamlit (interface web)
streamlit run main.py

# Mode console (développement)
python main.py
```

---

## 8. Exemples d'Interactions

### 8.1 Requête de localisation

```
Utilisateur: "Où puis-je jeter mes déchets près de la cafétéria ?"
Assistant: "📍 À gauche de la sortie de la cafétéria, à côté de la fontaine.

ℹ L'entrée principale est en face du bâtiment D."
```

### 8.2 Question sur le recyclage

```
Utilisateur: "Comment recycler une bouteille en plastique ?"
Assistant: "✅ Oui, les bouteilles en plastique vont dans le bac de recyclage.

💡 Pensez à retirer le bouchon et à rincer la bouteille avant de la jeter."
```

### 8.3 Requête approximative avec suggestions

```
Utilisateur: "Comment faire avec les déchets électroniques ?"
Assistant: "🤔 Je ne suis pas sûr de comprendre. Voici des suggestions :
• Où jeter les piles usagées ?
• Comment recycler un ordinateur ?
• Que faire des téléphones cassés ?"
```

---

## 9. Extensions Possibles

### 9.1 Améliorations techniques

- **Modèles multilingues** : Support de l'anglais et de l'arabe
- **Reconnaissance vocale** : Intégration avec speech-to-text
- **Base de données relationnelle** : Migration vers PostgreSQL/MySQL
- **API REST** : Exposition des fonctionnalités via API
- **Analyse de sentiment** : Détection de la satisfaction utilisateur

### 9.2 Fonctionnalités avancées

- **Géolocalisation** : Intégration GPS pour localisation automatique
- **Notifications push** : Alertes pour collectes de déchets
- **Gamification** : Système de points et badges pour encourager le tri
- **Réalité augmentée** : Overlay d'informations via caméra smartphone
- **Prédictions IA** : Anticipation des besoins basée sur l'historique

---

## 10. Maintenance et Support

### 10.1 Mise à jour des données

Les fichiers JSON peuvent être mis à jour sans redémarrage :

```python
# Rechargement dynamique des données
def reload_data(self):
    """Recharge les données depuis les fichiers JSON"""
    self.faq, self.locations = load_data()
    self.faq_vectors = np.array([nlp(q).vector for q in self.faq.keys()])
    self.vector_cache.clear()  # Vide le cache
```

### 10.2 Monitoring

```python
def get_performance_stats(self):
    """Retourne les statistiques de performance"""
    return {
        'total_queries': sum(self.stats.values()),
        'success_rate': (self.stats['faq_queries'] + self.stats['location_queries']) / sum(self.stats.values()),
        'cache_hits': len(self.vector_cache),
        'average_confidence': self.calculate_average_confidence()
    }
```

### 10.3 Debug et logs

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_query(self, query):
    logger.info(f"Processing query: {query}")
    # ... traitement
    logger.info(f"Response generated with confidence: {confidence}")
```

---

Cette documentation technique fournit une base solide pour comprendre, maintenir et étendre le chatbot Smart Waste Detection. Le système est conçu pour être facilement configurable et extensible selon les besoins spécifiques de votre environnement.
