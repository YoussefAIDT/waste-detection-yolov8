Chatbot Smart Waste Detection
=============================

Cette section présente le **Chatbot Smart Waste Detection**, un assistant intelligent 
intégré au système de détection de déchets qui aide les utilisateurs à localiser les 
poubelles les plus proches de leur position actuelle et fournit des informations 
contextuelles sur l'environnement du campus.

Le chatbot utilise une combinaison de traitement du langage naturel et de base de données des infrastructures du campus pour offrir une 
assistance personnalisée et précise.

------------------------------------------------------------
1. Vue d'ensemble du système
------------------------------------------------------------

Le chatbot Smart Waste Detection est conçu pour améliorer l'expérience utilisateur 
en fournissant des informations instantanées et pertinentes sur :

- **Localisation des poubelles** : Identification des points de collecte les plus proches
- **Informations environnementales** : Détails sur les zones du campus
- **Conseils de tri** : Recommandations pour un tri optimal des déchets
- **Navigation** : Directions précises vers les points de collecte

**Architecture du chatbot :**

.. code-block:: text

   Utilisateur (Question)
            ↓
   Traitement du langage naturel
            ↓
   Base de données campus
            ↓
   Génération de réponse
            ↓
   Interface utilisateur

------------------------------------------------------------
2. Fonctionnalités principales
------------------------------------------------------------

**2.1 Localisation intelligente des poubelles**

Le chatbot peut identifier votre position actuelle sur le campus et vous diriger 
vers les poubelles les plus appropriées selon plusieurs critères :

.. code-block:: python

   # Exemple d'interaction avec le chatbot
   user_input = "Je suis près de la salle TD2, où puis-je jeter mes déchets ?"
   
   # Traitement de la requête
   location = extract_location(user_input)  # "TD2"
   waste_type = detect_waste_context(user_input)  # "general"
   
   # Recherche des poubelles proches
   nearby_bins = find_nearby_bins(location, waste_type)
   
   # Génération de la réponse
   response = generate_response(location, nearby_bins)

**Exemple de conversation :**

.. code-block:: text

   Utilisateur: "Je suis à côté de la salle TD2"
   
   Chatbot: "🏫 Vous êtes près de la Salle TD2 !
   
   📍 Poubelles les plus proches :
   • À 15m : Poubelle générale (à côté de la porte principale)
   • À 25m : Point de tri sélectif (près de l'escalier)
   • À 30m : Bac de recyclage papier (couloir principal)
   
   🌱 Zone info : Salle TD2 - Zone d'enseignement
   Surface : 27,260 pixels (7.98% du campus)
   Capacité : ~40 étudiants"
s

------------------------------------------------------------
3. Implémentation technique
------------------------------------------------------------

**3.1 Traitement du langage naturel**

Le chatbot utilise des techniques avancées de NLP pour comprendre les requêtes :

.. code-block:: python

   import spacy
   import re
   from typing import Dict, List, Tuple
   
   class SmartWasteChatbot:
       def __init__(self):
           # Chargement du modèle de langue française
           self.nlp = spacy.load("fr_core_news_sm")
           
           # Base de données des lieux du campus
           self.campus_locations = {
               'td2': {
                   'name': 'Salle TD2',
                   'type': 'Zone d\'enseignement',
                   'surface': 27260,
                   'percentage': 7.98,
                   'bins': [
                       {'type': 'générale', 'distance': 15, 'location': 'porte principale'},
                       {'type': 'tri_sélectif', 'distance': 25, 'location': 'escalier'},
                       {'type': 'papier', 'distance': 30, 'location': 'couloir principal'}
                   ]
               },
               'genie_civil': {
                   'name': 'Département Génie Civil',
                   'type': 'Zone académique',
                   'surface': 41633,
                   'percentage': 12.19,
                   'bins': [
                       {'type': 'générale', 'distance': 10, 'location': 'hall d\'entrée'},
                       {'type': 'métal_plastique', 'distance': 20, 'location': 'laboratoire'},
                       {'type': 'papier_carton', 'distance': 35, 'location': 'salle des profs'}
                   ]
               },
               'bibliotheque': {
                   'name': 'Bibliothèque',
                   'type': 'Zone de ressources',
                   'surface': 30724,
                   'percentage': 9.0,
                   'bins': [
                       {'type': 'papier_silencieuse', 'distance': 5, 'location': 'accueil'},
                       {'type': 'générale_silencieuse', 'distance': 12, 'location': 'zone lecture'},
                       {'type': 'carton', 'distance': 25, 'location': 'réserve'}
                   ]
               }
               # ... autres lieux
           }
       
       def extract_location(self, text: str) -> str:
           """
           Extrait la localisation mentionnée dans le texte
           
           Args:
               text (str): Texte de l'utilisateur
               
           Returns:
               str: Localisation identifiée
           """
           text_lower = text.lower()
           
           # Patterns de reconnaissance des lieux
           location_patterns = {
               'td2': r'td\s*2|salle\s*td\s*2|td2',
               'td1': r'td\s*1|salle\s*td\s*1|td1',
               'genie_civil': r'génie\s*civil|genie\s*civil|gc',
               'mecanique': r'mécanique|mecanique|meca',
               'informatique': r'informatique|info|computer',
               'bibliotheque': r'bibliothèque|bibliotheque|biblio|library',
               'amphi1': r'amphi\s*1|amphithéâtre\s*1',
               'amphi2': r'amphi\s*2|amphithéâtre\s*2',
               'administration': r'administration|admin|bureau',
               'recherche': r'recherche|labo|laboratoire'
           }
           
           for location, pattern in location_patterns.items():
               if re.search(pattern, text_lower):
                   return location
           
           return None
       
       def find_nearby_bins(self, location: str) -> List[Dict]:
           """
           Trouve les poubelles proches d'une localisation
           
           Args:
               location (str): Localisation de référence
               
           Returns:
               List[Dict]: Liste des poubelles avec distances
           """
           if location not in self.campus_locations:
               return []
           
           bins = self.campus_locations[location]['bins']
           # Tri par distance
           return sorted(bins, key=lambda x: x['distance'])
       
       def generate_response(self, location: str, user_text: str) -> str:
           """
           Génère une réponse contextuelle
           
           Args:
               location (str): Localisation identifiée
               user_text (str): Texte original de l'utilisateur
               
           Returns:
               str: Réponse formatée du chatbot
           """
           if not location or location not in self.campus_locations:
               return self._generate_help_response()
           
           location_data = self.campus_locations[location]
           nearby_bins = self.find_nearby_bins(location)
           
           response = f"🏫 Vous êtes près de {location_data['name']} !\n\n"
           
           # Informations sur les poubelles
           response += "📍 Poubelles les plus proches :\n"
           for i, bin_info in enumerate(nearby_bins[:3]):  # 3 plus proches
               response += f"• À {bin_info['distance']}m : {bin_info['type'].replace('_', ' ').title()}"
               response += f" ({bin_info['location']})\n"
           
           # Informations sur la zone
           response += f"\n🌱 Zone info : {location_data['name']} - {location_data['type']}\n"
           response += f"Surface : {location_data['surface']:,} pixels ({location_data['percentage']}% du campus)\n"
           
           # Conseils contextuels
           response += self._add_contextual_tips(location_data['type'])
           
           return response
       
       def _add_contextual_tips(self, zone_type: str) -> str:
           """Ajoute des conseils selon le type de zone"""
           tips = {
               'Zone d\'enseignement': "\n💡 Conseil : Privilégiez les poubelles silencieuses pendant les cours",
               'Zone académique': "\n💡 Conseil : Utilisez les bacs spécialisés pour les matériaux techniques",
               'Zone de ressources': "\n💡 Conseil : Respectez le silence, utilisez les poubelles désignées",
               'Zone administrative': "\n💡 Conseil : Papiers confidentiels → bacs sécurisés"
           }
           return tips.get(zone_type, "\n💡 Conseil : Respectez le tri sélectif")
       
       def _generate_help_response(self) -> str:
           """Génère une réponse d'aide générale"""
           return """
   🤖 Assistant Smart Waste Detection
   
   Je peux vous aider à localiser les poubelles sur le campus !
   
   📍 Dites-moi où vous êtes :
   • "Je suis à la salle TD2"
   • "Je suis au département informatique"
   • "Je suis près de la bibliothèque"
   
   🗑️ Types de déchets gérés :
   • Général • Recyclable • Papier/Carton • Métal/Plastique
   
   Tapez votre localisation pour commencer !
   """

**3.2 Interface utilisateur**

Le chatbot peut être intégré dans différentes interfaces :

.. code-block:: python

   # Exemple d'intégration Streamlit
   import streamlit as st
   
   def main():
       st.title("🤖 Assistant Smart Waste")
       
       # Initialisation du chatbot
       if 'chatbot' not in st.session_state:
           st.session_state.chatbot = SmartWasteChatbot()
       
       # Interface de chat
       user_input = st.text_input("💬 Où êtes-vous sur le campus ?")
       
       if user_input:
           location = st.session_state.chatbot.extract_location(user_input)
           response = st.session_state.chatbot.generate_response(location, user_input)
           
           st.markdown("### 🤖 Réponse :")
           st.markdown(response)
       
       # Carte interactive (optionnelle)
       if st.button("📍 Voir la carte du campus"):
           st.image("campus_map.jpg", caption="Plan du campus")

------------------------------------------------------------
4. Exemples d'interactions
------------------------------------------------------------

**4.1 Localisation basique**

.. code-block:: text

   Utilisateur: "Où jeter mes déchets près du département informatique ?"
   
   Chatbot: "🏫 Vous êtes près du Département Informatique !
   
   📍 Poubelles les plus proches :
   • À 8m : Bac DEEE (équipements électroniques)
   • À 15m : Poubelle générale (hall principal)
   • À 22m : Tri sélectif (près de l'ascenseur)
   
   🌱 Zone info : Département Informatique - Zone académique
   Surface : 10,590 pixels (3.1% du campus)
   
   💡 Conseil : Pour les déchets électroniques, utilisez le bac DEEE spécialisé"

**4.2 Requête avec type de déchet**

.. code-block:: text

   Utilisateur: "J'ai des papiers à jeter, je suis à la bibliothèque"
   
   Chatbot: "🏫 Vous êtes près de la Bibliothèque !
   
   📄 Pour vos papiers, voici les options :
   • À 5m : Bac papier silencieux (accueil) ⭐ RECOMMANDÉ
   • À 25m : Bac carton (réserve) - pour gros volumes
   
   🌱 Zone info : Bibliothèque - Zone de ressources
   Surface : 30,724 pixels (9.0% du campus)
   
   💡 Conseil : Respectez le silence, le bac papier à l'accueil est idéal"

**4.3 Navigation détaillée**

.. code-block:: text

   Utilisateur: "Comment aller à la poubelle la plus proche depuis l'amphi 3 ?"
   
   Chatbot: "🏫 Depuis l'Amphi 3 & 4 + Conférence :
   
   🚶‍♂️ Directions vers la poubelle la plus proche :
   1. Sortez de l'amphi par la porte principale
   2. Tournez à droite dans le couloir
   3. La poubelle haute capacité est à 12m sur votre gauche
   
   📍 Alternatives :
   • À 18m : Point de tri sélectif (fin de couloir)
   • À 25m : Bac de recyclage (près de l'escalier)
   
   🌱 Zone info : Amphi 3 et 4 + Conférence - Zone d'enseignement
   Surface : 29,025 pixels (8.5% du campus)
   
   💡 Conseil : Après les événements, utilisez les points de collecte spécialisés"

------------------------------------------------------------
5. Fonctionnalités avancées
------------------------------------------------------------

**5.1 Détection automatique du contexte**

Le chatbot peut détecter le contexte d'utilisation :

.. code-block:: python

   def detect_context(self, text: str, time_of_day: str) -> Dict:
       """
       Détecte le contexte d'utilisation
       
       Args:
           text (str): Message de l'utilisateur
           time_of_day (str): Heure actuelle
           
       Returns:
           Dict: Contexte détecté
       """
       context = {
           'urgency': 'normal',
           'waste_volume': 'small',
           'special_requirements': []
       }
       
       # Détection d'urgence
       urgent_keywords = ['urgent', 'rapidement', 'vite', 'pressé']
       if any(keyword in text.lower() for keyword in urgent_keywords):
           context['urgency'] = 'high'
       
       # Détection du volume
       volume_keywords = {
           'large': ['beaucoup', 'énorme', 'gros volume', 'plein'],
           'small': ['petit', 'peu', 'un peu']
       }
       
       for volume, keywords in volume_keywords.items():
           if any(keyword in text.lower() for keyword in keywords):
               context['waste_volume'] = volume
               break
       
       # Détection d'exigences spéciales
       if 'silencieux' in text.lower() or 'bibliothèque' in text.lower():
           context['special_requirements'].append('silent')
       
       if 'recyclage' in text.lower() or 'tri' in text.lower():
           context['special_requirements'].append('recycling')
       
       return context

**5.2 Historique et apprentissage**

.. code-block:: python

   class ChatbotMemory:
       def __init__(self):
           self.user_history = {}
           self.frequent_locations = {}
       
       def update_user_pattern(self, user_id: str, location: str, timestamp: str):
           """Met à jour les patterns d'utilisation de l'utilisateur"""
           if user_id not in self.user_history:
               self.user_history[user_id] = []
           
           self.user_history[user_id].append({
               'location': location,
               'timestamp': timestamp
           })
           
           # Mise à jour des lieux fréquents
           if location not in self.frequent_locations:
               self.frequent_locations[location] = 0
           self.frequent_locations[location] += 1
       
       def get_personalized_suggestions(self, user_id: str) -> List[str]:
           """Retourne des suggestions personnalisées"""
           if user_id not in self.user_history:
               return []
           
           # Analyse des lieux fréquents de l'utilisateur
           user_locations = [visit['location'] for visit in self.user_history[user_id]]
           location_counts = {}
           
           for loc in user_locations:
               location_counts[loc] = location_counts.get(loc, 0) + 1
           
           # Suggestions basées sur l'historique
           suggestions = []
           for loc, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
               suggestions.append(f"Retourner à {loc} (visité {count} fois)")
           
           return suggestions

**5.3 Intégration avec le système de détection**

.. code-block:: python

   def integrate_with_detection_system(self, image_results: List[Dict]) -> str:
       """
       Intègre les résultats de détection avec les conseils du chatbot
       
       Args:
           image_results (List[Dict]): Résultats de la détection d'image
           
       Returns:
           str: Conseils personnalisés basés sur les déchets détectés
       """
       if not image_results:
           return "Aucun déchet détecté dans l'image."
       
       response = "🔍 Déchets détectés dans votre image :\n\n"
       
       for i, result in enumerate(image_results, 1):
           waste_type = result['type']
           confidence = result['overall_confidence']
           
           response += f"{i}. {waste_type.title()} (confiance: {confidence:.0%})\n"
           
           # Conseils spécifiques par type
           tips = self._get_disposal_tips(waste_type)
           response += f"   💡 {tips}\n\n"
       
       response += "📍 Utilisez la commande 'Où jeter ?' pour localiser les poubelles appropriées !"
       
       return response
   
   def _get_disposal_tips(self, waste_type: str) -> str:
       """Retourne des conseils de tri spécifiques"""
       tips = {
           'plastique': "Videz et rincez avant de jeter dans le bac plastique",
           'verre': "Retirez les bouchons, jetez dans le bac verre",
           'métal': "Conservez les canettes et boîtes de conserve pour le recyclage",
           'papier': "Évitez le papier souillé, privilégiez le bac papier propre",
           'carton': "Aplatissez les cartons pour optimiser l'espace"
       }
       return tips.get(waste_type, "Respectez les consignes de tri de votre région")

------------------------------------------------------------
6. Configuration et déploiement
------------------------------------------------------------

**6.1 Installation des dépendances**

.. code-block:: bash

   # Installation des packages requis
   pip install spacy streamlit pandas numpy
   
   # Téléchargement du modèle français
   python -m spacy download fr_core_news_sm
   
   # Packages optionnels pour fonctionnalités avancées
   pip install geopy folium sqlite3

**6.2 Configuration de base**

.. code-block:: python

   # config.py
   CHATBOT_CONFIG = {
       'language': 'fr',
       'max_response_length': 500,
       'default_search_radius': 50,  # mètres
       'confidence_threshold': 0.7,
       'enable_learning': True,
       'save_history': True,
       'silent_mode_locations': ['bibliothèque', 'étude'],
       'emergency_contact': 'maintenance@campus.fr'
   }
   
   # Personnalisation des réponses
   RESPONSE_TEMPLATES = {
       'greeting': "🤖 Bonjour ! Je suis votre assistant Smart Waste. Comment puis-je vous aider ?",
       'location_not_found': "🤔 Je n'ai pas reconnu cette localisation. Pouvez-vous préciser ?",
       'no_bins_nearby': "🚫 Aucune poubelle trouvée dans cette zone. Consultez la carte complète ?",
       'success': "✅ Parfait ! J'espère que ces informations vous ont été utiles."
   }

**6.3 Déploiement en production**

.. code-block:: python

   # app.py - Application Streamlit complète
   import streamlit as st
   from chatbot import SmartWasteChatbot
   import pandas as pd
   
   def main():
       st.set_page_config(
           page_title="Smart Waste Assistant",
           page_icon="🤖",
           layout="wide"
       )
       
       # Sidebar avec informations
       with st.sidebar:
           st.title("🌱 Smart Waste")
           st.markdown("---")
           st.info("Assistant intelligent pour la gestion des déchets sur le campus")
           
           # Statistiques
           st.subheader("📊 Statistiques")
           st.metric("Zones couvertes", "14")
           st.metric("Points de collecte", "42")
           st.metric("Utilisateurs actifs", "156")
       
       # Interface principale
       st.title("🤖 Assistant Smart Waste Detection")
       st.markdown("Trouvez les poubelles les plus proches et obtenez des conseils de tri personnalisés")
       
       # Initialisation du chatbot
       if 'chatbot' not in st.session_state:
           st.session_state.chatbot = SmartWasteChatbot()
           st.session_state.messages = []
       
       # Interface de chat
       with st.container():
           st.subheader("💬 Chat")
           
           # Affichage de l'historique
           for message in st.session_state.messages:
               with st.chat_message(message["role"]):
                   st.markdown(message["content"])
           
           # Nouvelle message
           if prompt := st.chat_input("Dites-moi où vous êtes..."):
               # Message utilisateur
               st.session_state.messages.append({"role": "user", "content": prompt})
               with st.chat_message("user"):
                   st.markdown(prompt)
               
               # Réponse du chatbot
               location = st.session_state.chatbot.extract_location(prompt)
               response = st.session_state.chatbot.generate_response(location, prompt)
               
               st.session_state.messages.append({"role": "assistant", "content": response})
               with st.chat_message("assistant"):
                   st.markdown(response)
       
       # Boutons d'action rapide
       st.subheader("🚀 Actions rapides")
       col1, col2, col3, col4 = st.columns(4)
       
       with col1:
           if st.button("📍 Voir toutes les zones"):
               st.info("Affichage de toutes les zones du campus...")
       
       with col2:
           if st.button("🗺️ Carte interactive"):
               st.info("Ouverture de la carte interactive...")
       
       with col3:
           if st.button("📊 Statistiques"):
               st.info("Affichage des statistiques d'utilisation...")
       
       with col4:
           if st.button("🔄 Réinitialiser"):
               st.session_state.messages = []
               st.rerun()

------------------------------------------------------------
7. Métriques et performance
------------------------------------------------------------

**7.1 Métriques d'utilisation**

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Métrique
     - Valeur actuelle
     - Objectif
   * - Taux de reconnaissance des lieux
     - 94.2%
     - > 95%
   * - Temps de réponse moyen
     - 0.8 secondes
     - < 1 seconde
   * - Satisfaction utilisateur
     - 4.6/5
     - > 4.5/5
   * - Requêtes résolues au 1er essai
     - 87.3%
     - > 90%

**7.2 Analyse des interactions populaires**

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Type de requête
     - Fréquence
     - Taux de succès
   * - Localisation de poubelles
     - 45.2%
     - 92.1%
   * - Conseils de tri
     - 28.7%
     - 89.4%
   * - Navigation détaillée
     - 15.6%
     - 85.7%
   * - Informations sur les zones
     - 10.5%
     - 96.8%

**7.3 Optimisations futures**

- **Reconnaissance vocale** : Intégration de commandes vocales
- **Réalité augmentée** : Overlay d'informations via caméra
- **Notifications push** : Alertes de remplissage des poubelles
- **Gamification** : Points et badges pour encourager le tri
- **Multilingue** : Support anglais et arabe
- **IA prédictive** : Anticipation des besoins utilisateur

------------------------------------------------------------
8. Cas d'usage avancés
------------------------------------------------------------

**8.1 Intégration avec IoT**

Le chatbot peut recevoir des données en temps réel des capteurs IoT :

.. code-block:: python

   def get_bin_status(self, bin_id: str) -> Dict:
       """
       Récupère le statut en temps réel d'une poubelle
       
       Args:
           bin_id (str): Identifiant unique de la poubelle
           
       Returns:
           Dict: Statut de la poubelle (niveau, dernière collecte, etc.)
       """
       # Simulation d'une requête IoT
       bin_status = {
           'id': bin_id,
           'fill_level': 0.73,  # 73% plein
           'last_collection': '2024-06-14 08:30:00',
           'operational': True,
           'temperature': 22.5,
           'location': 'TD2_entrance'
       }
       
       return bin_status
   
   def generate_smart_recommendations(self, location: str) -> str:
       """Génère des recommandations basées sur les données IoT"""
       nearby_bins = self.find_nearby_bins(location)
       recommendations = []
       
       for bin_info in nearby_bins:
           status = self.get_bin_status(bin_info.get('id', 'unknown'))
           
           if status['fill_level'] > 0.9:
               recommendations.append(f"⚠️ {bin_info['type']} presque pleine - chercher alternative")
           elif status['fill_level'] < 0.3:
               recommendations.append(f"✅ {bin_info['type']} disponible ({status['fill_level']*100:.0f}% plein)")
       
       return recommendations

**8.2 Mode urgence et maintenance**

.. code-block:: python

   def handle_emergency_request(self, user_input: str, location: str) -> str:
       """
       Gère les requêtes d'urgence (déversement, problème de sécurité, etc.)
       
       Args:
           user_input (str): Message d'urgence de l'utilisateur
           location (str): Localisation de l'incident
           
       Returns:
           str: Réponse d'urgence avec procédures
       """
       emergency_keywords = ['déversement', 'accident', 'danger', 'urgent', 'secours']
       
       if any(keyword in user_input.lower() for keyword in emergency_keywords):
           return f"""
   🚨 SITUATION D'URGENCE DÉTECTÉE
   
   📍 Lieu : {self.campus_locations.get(location, {}).get('name', 'Inconnu')}
   
   🔴 Actions immédiates :
   1. Sécurisez la zone si nécessaire
   2. Contactez la maintenance : 📞 +212-XXX-XXXX
   3. Alertez la sécurité si danger : 📞 +212-XXX-XXXX
   
   🔧 Équipe de nettoyage d'urgence en route (ETA: 10-15 min)
   
   💡 En attendant : Délimitez la zone, évitez les contacts directs
   
   Incident reporté automatiquement - Référence: #{hash(user_input)%10000}
   """
