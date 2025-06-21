# Projet : Gestionnaire d'Objectifs d'Épargne

#Ce projet est une application développée avec **Streamlit** qui permet à l'utilisateur de :

- Ajouter un objectif d’épargne
- Modifier ou supprimer un objectif existant
- Visualiser la liste des objectifs
- Sauvegarder les données dans une base SQLite

---

##  Outils utilisés

- Python 3.10
- Streamlit
- SQLite3
- Pandas
- Plotly

---

## Lancer le projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/Souleykeita/projet-Keita-Belguith.git
cd projet-Keita-Belguith

# 2. Créer un environnement virtuel
python -m venv env
env\Scripts\activate       # Sur Windows

#3 installé les depandances
pip install streamlit pandas plotly


# 4 Lancer streamlit
streamlit run main.py

# Structure du projet

#-main.py                Fichier principal Streamlit
# forms.py               Gestion des formulaires
#-models.py              Structure des données
#-service.py             Fonctions métiers
#-epargne.db            Base de données SQLite
#-README.md              Ce fichier
#-ua.jpg                 Logo


### Auteurs ###

#Souleymane KEITA & Zayneb BELGUITH
#Master 2 Ingénierie des Données et Évaluation Économétrique
#Université d’Angers