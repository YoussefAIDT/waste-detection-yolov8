========================================
Chatbot Smart Waste Detection
========================================

Documentation Technique
=========================

Cette documentation présente le **Chatbot Smart Waste Detection**, un assistant intelligent 
utilisant le traitement du langage naturel (NLP) pour aider les utilisateurs à localiser 
les points de collecte de déchets et obtenir des conseils de tri personnalisés sur le campus.

Le chatbot combine SpaCy, scikit-learn et Streamlit pour offrir une expérience utilisateur 
optimale avec une compréhension contextuelle avancée des requêtes.

------------------------------------------------------------
1. Architecture du Système
------------------------------------------------------------

1.1 Vue d'ensemble
==================

Le chatbot combine plusieurs technologies avancées :

- **Traitement du langage naturel** : SpaCy avec modèles français optimisés
- **Similarité sémantique** : Calcul de similarité cosinus pour la compréhension des requêtes
- **Base de données dynamique** : Stockage JSON des FAQ et localisations
- **Interface utilisateur** : Streamlit pour une expérience interactive
- **Système de cache** : Optimisation des performances avec mise en cache des embeddings

**Flux de traitement :**

.. code-block:: text

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

1.2 Composants principaux
=========================

**WasteChatbot** : Classe principale gérant :

- Traitement des requêtes utilisateur
- Recherche de correspondances dans la FAQ
- Gestion des requêtes de localisation
- Système de suggestions intelligentes
- Journalisation des conversations

------------------------------------------------------------
2. Fonctionnalités Techniques
------------------------------------------------------------

2.1 Système de traitement NLP
=============================

.. code-block:: python

   # Chargement du modèle NLP avec fallback intelligent
   try:
       nlp = spacy.load("fr_dep_news_trf")  # Modèle transformer haute précision
   except:
       nlp = spacy.load("fr_core_news_md")  # Fallback si transformer indisponible
       print("Utilisation du modèle md (le modèle transformer n'est pas installé)")

**Caractéristiques :**

- Support prioritaire des modèles transformer pour une meilleure précision
- Fallback automatique vers des modèles standards
- Traitement optimisé des requêtes en français
- Extraction automatique d'entités et de contexte

2.2 Normalisation et synonymes
==============================

Le système intègre une normalisation intelligente du texte :

.. code-block:: python

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

**Avantages :**

- Gestion des variantes linguistiques
- Normalisation des termes techniques
- Suppression du bruit textuel
- Amélioration de la précision des correspondances

2.3 Système de similarité sémantique
====================================

**Algorithme de correspondance :**

- Utilisation de la similarité cosinus entre vecteurs de mots
- Seuil de confiance ajustable (0.72 par défaut)
- Cache des embeddings pour optimiser les performances
- Recherche dans la FAQ et les localisations

.. code-block:: python

   def find_best_match(self, query):
       """Trouve la meilleure correspondance avec score de confiance"""
       query_vec = self.get_embedding(query)
       similarities = cosine_similarity([query_vec], faq_vectors)[0]
       best_idx = np.argmax(similarities)
       return questions[best_idx], similarities[best_idx]

   def get_embedding(self, text):
       """Cache les embeddings pour améliorer les performances"""
       if text not in self.vector_cache:
           self.vector_cache[text] = nlp(text).vector
       return self.vector_cache[text]

------------------------------------------------------------
3. Gestion des Données
------------------------------------------------------------

3.1 Structure des fichiers de données
=====================================

Le système utilise des fichiers JSON pour une gestion flexible des données :

**data/faq.json :**

.. code-block:: json

   {
       "Puis-je recycler une bouteille en plastique ?": "✅ Oui, les bouteilles en plastique vont dans le bac de recyclage.",
       "Où jeter les déchets organiques ?": "🥬 Les déchets organiques vont dans le composteur du jardin.",
       "Comment trier le verre ?": "🍾 Le verre va dans les conteneurs spécialisés, retirez les bouchons."
   }

**data/locations.json :**

.. code-block:: json

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

3.2 Chargement dynamique des données
====================================

.. code-block:: python

   def load_data():
       data_dir = Path("data")
       faq_path = data_dir / "faq.json"
       locations_path = data_dir / "locations.json"
       
       # Création du dossier si inexistant
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

**Fonctionnalités :**

- Création automatique des fichiers manquants
- Gestion des erreurs de lecture
- Encodage UTF-8 pour le support des caractères spéciaux
- Structure modulaire pour faciliter les mises à jour

------------------------------------------------------------
4. Classe WasteChatbot
------------------------------------------------------------

4.1 Initialisation et configuration
===================================

.. code-block:: python

   class WasteChatbot:
       def __init__(self):
           self.faq = faq
           self.locations = locations
           self.conversation_history = []
           self.threshold = 0.72  # Seuil de similarité ajustable
           
           # Cache pour les embeddings
           self.vector_cache = {}
           
           # Statistiques d'utilisation
           self.stats = defaultdict(int)

**Paramètres configurables :**

- ``threshold`` : Seuil de confiance pour les correspondances (défaut: 0.72)
- ``vector_cache`` : Cache des embeddings pour optimiser les performances
- ``stats`` : Collecte de métriques d'utilisation

4.2 Traitement des requêtes principales
=======================================

.. code-block:: python

   def process_query(self, query):
       """Traite une requête utilisateur"""
       # Vérification des lieux en premier
       location_info = self.handle_location_query(query)
       if location_info:
           self.stats['location_queries'] += 1
           return (
               f"{location_info['poubelle']}\n\n"
               f"ℹ {location_info['entrée']}"
           )
       
       # Recherche dans la FAQ
       best_question, confidence = self.find_best_match(query)
       
       if confidence > self.threshold:
           self.stats['faq_queries'] += 1
           return self.faq[best_question]
       else:
           self.stats['unknown_queries'] += 1
           return self._generate_suggestions(query)

4.3 Gestion des requêtes de localisation
========================================

.. code-block:: python

   def handle_location_query(self, query):
       """Gestion améliorée des requêtes de localisation"""
       query = normalize_text(query)
       best_match = None
       best_score = 0
       
       for location in self.locations:
           loc_norm = normalize_text(location)
           if loc_norm in query:  # Correspondance exacte
               return self.locations[location]
           
           # Similarité sémantique pour les requêtes approximatives
           score = cosine_similarity(
               [self.get_embedding(location)],
               [self.get_embedding(query)]
           )[0][0]
           
           if score > best_score:
               best_score = score
               best_match = location
       
       if best_score > 0.65:  # Seuil pour les correspondances approximatives
           return self.locations[best_match]
       
       return None

**Algorithme de localisation :**

1. **Correspondance exacte** : Recherche directe du lieu dans la requête
2. **Similarité sémantique** : Calcul de similarité pour les requêtes approximatives
3. **Seuil adaptatif** : 0.65 pour les correspondances de localisation (plus permissif)

------------------------------------------------------------
5. Interface Utilisateur
------------------------------------------------------------

5.1 Interface Streamlit
=======================

**Fonctionnalités :**

- Chat interactif avec historique des conversations
- Interface responsive et intuitive
- Gestion d'état avec ``st.session_state``
- Indicateurs de progression pour les recherches

.. code-block:: python

   def run_chatbot():
       import streamlit as st
       
       if 'chatbot' not in st.session_state:
           st.session_state.chatbot = WasteChatbot()
       
       st.title("♻ Assistant Intelligent de Tri des Déchets")
       st.markdown("Posez vos questions sur le recyclage ou la localisation des poubelles")
       
       # Historique de conversation
       if 'history' not in st.session_state:
           st.session_state.history = []
       
       # Affichage de l'historique
       for msg in st.session_state.history:
           with st.chat_message(msg['role']):
               st.markdown(msg['content'])
       
       # Entrée utilisateur
       if prompt := st.chat_input("Votre question..."):
           # Traitement et affichage de la réponse
           with st.spinner("Recherche en cours..."):
               response = st.session_state.chatbot.process_query(prompt)
               st.session_state.chatbot.log_conversation(prompt, response)

5.2 Mode console
================

Pour les tests et le développement :

.. code-block:: python

   if __name__ == "__main__":
       from datetime import datetime
       
       print("👋 Bonjour ! Posez-moi vos questions sur le tri des déchets.")
       chatbot = WasteChatbot()
       
       while True:
           query = input("Vous: ")
           if query.lower() in ['exit', 'quit', 'bye']:
               break
           
           response = chatbot.process_query(query)
           print(f"Assistant: {response}")

------------------------------------------------------------
6. Système de Suggestions
------------------------------------------------------------

6.1 Génération de suggestions intelligentes
===========================================

Quand la confiance est faible, le système propose des alternatives :

.. code-block:: python

   def _generate_suggestions(self, query):
       """Génère des suggestions quand la confiance est faible"""
       # Recherche de questions similaires
       similar_questions = [
           q for q in questions 
           if cosine_similarity(
               [self.get_embedding(q)],
               [self.get_embedding(query)]
           )[0][0] > 0.5
       ][:3]
       
       response = "🤔 Je ne suis pas sûr de comprendre. Voici des suggestions :\n"
       response += "\n".join(f"• {q}" for q in similar_questions)
       return response

**Algorithme de suggestions :**

1. Calcul de similarité avec toutes les questions FAQ
2. Filtrage avec seuil de 0.5 (plus permissif)
3. Limitation à 3 suggestions maximum
4. Présentation formatée avec émojis

6.2 Système de fallback
=======================

En cas d'absence de suggestions pertinentes :

.. code-block:: python

   def _generate_help_response(self):
       """Génère une réponse d'aide générale"""
       return """
   🤖 Assistant Smart Waste Detection
   
   Je peux vous aider avec :
   
   📍 Localisation des poubelles :
   • "Où jeter mes déchets près de la cafétéria ?"
   • "Poubelle la plus proche de la bibliothèque ?"
   
   ♻️ Questions sur le recyclage :
   • "Comment recycler une bouteille en plastique ?"
   • "Où jeter les déchets organiques ?"
   
   Posez votre question !
   """

------------------------------------------------------------
7. Optimisations et Performances
------------------------------------------------------------

7.1 Système de cache
====================

.. code-block:: python

   def get_embedding(self, text):
       """Cache les embeddings pour améliorer les performances"""
       if text not in self.vector_cache:
           self.vector_cache[text] = nlp(text).vector
       return self.vector_cache[text]

**Avantages du cache :**

- Réduction du temps de calcul des embeddings
- Amélioration des performances pour les requêtes répétées
- Optimisation de la mémoire avec réutilisation des vecteurs

7.2 Statistiques d'utilisation
==============================

Le chatbot collecte des métriques pour l'amélioration continue :

.. code-block:: python

   # Initialisation des statistiques
   self.stats = defaultdict(int)

   # Tracking par type de requête
   self.stats['location_queries'] += 1  # Requêtes de localisation
   self.stats['faq_queries'] += 1       # Questions FAQ
   self.stats['unknown_queries'] += 1   # Requêtes non comprises

**Métriques collectées :**

- ``location_queries`` : Nombre de requêtes de localisation
- ``faq_queries`` : Nombre de questions FAQ traitées
- ``unknown_queries`` : Nombre de requêtes non comprises

7.3 Journalisation
==================

.. code-block:: python

   def log_conversation(self, query, response):
       """Journalisation des conversations"""
       self.conversation_history.append({
           'query': query,
           'response': response,
           'timestamp': datetime.now().isoformat()
       })

**Données journalisées :**

- Requête utilisateur originale
- Réponse générée par le chatbot
- Horodatage de l'interaction
- Possibilité d'analyse post-traitement

------------------------------------------------------------
8. Installation et Configuration
------------------------------------------------------------

8.1 Dépendances requises
========================

.. code-block:: bash

   # Installation des packages principaux
   pip install spacy scikit-learn numpy streamlit

   # Téléchargement des modèles français
   python -m spacy download fr_core_news_md
   python -m spacy download fr_dep_news_trf  # Optionnel, pour de meilleures performances

**Packages requis :**

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Package
     - Version minimale
     - Utilisation
   * - spacy
     - >= 3.4
     - Traitement du langage naturel
   * - scikit-learn
     - >= 1.0
     - Calcul de similarité cosinus
   * - numpy
     - >= 1.21
     - Opérations sur les vecteurs
   * - streamlit
     - >= 1.25
     - Interface utilisateur web



------------------------------------------------------------
9. Exemples d'Interactions
------------------------------------------------------------

9.1 Requête de localisation
===========================

.. code-block:: text

   Utilisateur: "Où puis-je jeter mes déchets près de la cafétéria ?"
   
   Assistant: "📍 À gauche de la sortie de la cafétéria, à côté de la fontaine.

   ℹ L'entrée principale est en face du bâtiment D."

9.2 Question sur le recyclage
=============================

.. code-block:: text

   Utilisateur: "Comment recycler une bouteille en plastique ?"
   
   Assistant: "✅ Oui, les bouteilles en plastique vont dans le bac de recyclage."

9.3 Requête approximative avec suggestions
==========================================

.. code-block:: text

   Utilisateur: "Comment faire avec les déchets électroniques ?"
   
   Assistant: "🤔 Je ne suis pas sûr de comprendre. Voici des suggestions :
   • Où jeter les piles usagées ?
   • Comment recycler un ordinateur ?
   • Que faire des téléphones cassés ?"

9.4 Gestion des synonymes
=========================

.. code-block:: text

   Utilisateur: "Je suis près du TD 1, où jeter ?"
   
   # Normalisation automatique : "TD 1" → "td1"
   
   Assistant: "📍 Point de collecte TD1 : à droite de la salle, près de l'escalier.

   ℹ Accès par le couloir principal du bâtiment A."


------------------------------------------------------------
11. Conclusion
------------------------------------------------------------

Le **Chatbot Smart Waste Detection** offre une solution complète et évolutive pour l'assistance 
au tri des déchets sur campus. Sa conception modulaire permet une maintenance aisée et des 
extensions futures.

**Points forts :**

- Architecture robuste avec gestion d'erreurs
- Interface utilisateur intuitive
- Système de suggestions intelligent
- Performance optimisée avec cache
- Documentation complète et code commenté

**Utilisation recommandée :**

- Déploiement en mode Streamlit pour les utilisateurs finaux
- Mode console pour développement et tests
- Intégration possible avec d'autres systèmes via API

Ce chatbot constitue une base solide pour développer des assistants intelligents 
dans le domaine environnemental et peut être adapté à d'autres contextes d'utilisation.


📞 Contact & Support
-----------------------

.. raw:: html

   <div style="background-color: #28a745; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;">
      <div style="color: white; font-family: 'Arial', sans-serif;">
         <h3 style="margin: 0 0 15px 0; font-size: 1.4em; font-weight: bold;">
            Développé par Youssef ES-SAAIDI & Zakariae ZEMMAHI & Mohamed HAJJI
         </h3>
         <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; margin-top: 15px;">
            <div style="display: flex; align-items: center; gap: 8px;">
               <span style="font-size: 1.2em;">🐙</span>
               <a href="https://github.com/YoussefAIDT" target="_blank" style="color: #ffffff; text-decoration: none; font-weight: 500; padding: 5px 10px; background-color: rgba(255,255,255,0.2); border-radius: 5px; transition: all 0.3s ease;">
                  YoussefAIDT GitHub
               </a>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
               <span style="font-size: 1.2em;">🐙</span>
               <a href="https://github.com/zakariazemmahi" target="_blank" style="color: #ffffff; text-decoration: none; font-weight: 500; padding: 5px 10px; background-color: rgba(255,255,255,0.2); border-radius: 5px; transition: all 0.3s ease;">
                  zakariazemmahi GitHub
               </a>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
               <span style="font-size: 1.2em;">🐙</span>
               <a href="https://github.com/mohamedhajji11" target="_blank" style="color: #ffffff; text-decoration: none; font-weight: 500; padding: 5px 10px; background-color: rgba(255,255,255,0.2); border-radius: 5px; transition: all 0.3s ease;">
                  mohamedhajji11 GitHub
               </a>
            </div>
         </div>
      </div>
   </div>

.. raw:: html

   <style>
   div a:hover {
      background-color: rgba(255,255,255,0.3) !important;
      transform: translateY(-2px);
   }
   </style>
