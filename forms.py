# forms.py
import streamlit as st
from models import ObjectifEpargne

def formulaire_ajout():
    """Affiche le formulaire d'ajout d'un nouvel objectif d'épargne (dans la barre latérale).
       Retourne un dictionnaire avec les données saisies si le formulaire est soumis, sinon None."""
    # Placer le formulaire dans la barre latérale
    with st.sidebar:
        st.header("Nouvel objectif d’épargne")  # Titre du formulaire dans la sidebar
        # Définition du formulaire d'ajout
        with st.form(key="form_ajout", clear_on_submit=True):
            nom = st.text_input("Nom de l’objectif")
            montant_obj = st.number_input("Montant objectif (€)", min_value=0.0, format="%.2f")
            montant_act = st.number_input("Montant actuel épargné (€)", min_value=0.0, format="%.2f")
            submit = st.form_submit_button("Ajouter")
    # Si le bouton "Ajouter" du formulaire a été cliqué
    if submit:
        # Retourner les valeurs saisies sous forme de dictionnaire
        return {"nom": nom, "montant_objectif": montant_obj, "montant_actuel": montant_act}
    return None

def formulaire_modification(obj: ObjectifEpargne):
    """Affiche un formulaire de modification pour un objectif existant.
       Retourne un dictionnaire avec les nouvelles valeurs si soumis, sinon None."""
    st.subheader(f"Modifier l’objectif : {obj.nom}")
    with st.form(key="form_modif"):
        new_nom = st.text_input("Nom de l’objectif", value=obj.nom)
        new_cible = st.number_input("Montant objectif (€)", min_value=0.0, format="%.2f", value=obj.montant_objectif)
        new_actuel = st.number_input("Montant actuel épargné (€)", min_value=0.0, format="%.2f", value=obj.montant_actuel)
        submit = st.form_submit_button("Enregistrer")
    if submit:
        return {"nom": new_nom, "montant_objectif": new_cible, "montant_actuel": new_actuel}
    return None
