# main.py
import streamlit as st
from models import ObjectifEpargne
import service
import forms
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

# Initialisation de la base de données
service.init_db()

# Affichage du logo (s'il est à la racine du projet)
st.image("C:/Users/keita/Desktop/PROJET_Python/ua.jpg", width=150)

# Titre de l'application
st.title("Gestionnaire d’objectifs d’épargne")
st.write("Bienvenue ! Cette application vous aide à suivre vos objectifs d'épargne. "
         "Ajoutez de nouveaux objectifs, enregistrez vos progrès et atteignez vos buts financiers .")

# Charger les données depuis la base
conn = sqlite3.connect("objectifs.db")
df_stats = pd.read_sql_query("SELECT * FROM objectifs", conn)

# Calculs statistiques
total_epargne = df_stats["montant_actuel"].sum()
total_objectif = df_stats["montant_objectif"].sum()
pourcentage_global = (total_epargne / total_objectif) * 100 if total_objectif > 0 else 0
nb_objectifs = len(df_stats)
nb_atteints = df_stats[df_stats["montant_actuel"] >= df_stats["montant_objectif"]].shape[0]
montant_restant = max(0.0, total_objectif - total_epargne)

# Avancement
df_stats = df_stats[df_stats["montant_objectif"] > 0]
df_stats["taux_avancement"] = df_stats["montant_actuel"] / df_stats["montant_objectif"]
plus_avance = df_stats.loc[df_stats["taux_avancement"].idxmax()] if not df_stats.empty else None
plus_en_retard = df_stats.loc[df_stats["taux_avancement"].idxmin()] if not df_stats.empty else None

# Statistiques générales
st.header("📈 Statistiques générales")
st.markdown(f"""
-  **Total épargné :** {total_epargne:.2f} €  
-  **Total des objectifs :** {total_objectif:.2f} €  
-  **Progression globale :** {pourcentage_global:.1f} %  
-  **Objectifs atteints :** {nb_atteints} / {nb_objectifs}  
-  **Montant restant à épargner :** {montant_restant:.2f} €
""")

if plus_avance is not None:
    st.success(f"🏅 Objectif le plus avancé : **{plus_avance['nom']}** ({plus_avance['taux_avancement']*100:.1f} %)")
if plus_en_retard is not None:
    st.warning(f"🐌 Objectif le plus en retard : **{plus_en_retard['nom']}** ({plus_en_retard['taux_avancement']*100:.1f} %)")

# Diagramme camembert
if not df_stats.empty:
    fig_pie = px.pie(df_stats,
                     names="nom",
                     values="montant_actuel",
                     title="Répartition de l'épargne par objectif",
                     hole=0.4)
    st.plotly_chart(fig_pie)

# État session
if "mode_modif" not in st.session_state:
    st.session_state["mode_modif"] = False
    st.session_state["objectif_a_modifier"] = None

# Formulaire d'ajout
data_nouvel_obj = forms.formulaire_ajout()
if data_nouvel_obj:
    nouvel_obj = ObjectifEpargne(nom=data_nouvel_obj["nom"],
                                 montant_objectif=data_nouvel_obj["montant_objectif"],
                                 montant_actuel=data_nouvel_obj["montant_actuel"])
    obj_id = service.ajouter_objectif(nouvel_obj)
    service.ajouter_transaction(obj_id, nouvel_obj.montant_actuel)
    st.rerun()

# Formulaire de modification
if st.session_state["mode_modif"] and st.session_state["objectif_a_modifier"] is not None:
    obj_id = st.session_state["objectif_a_modifier"]
    objectif_a_modif = service.get_objectif(obj_id)
    if objectif_a_modif:
        data_modif = forms.formulaire_modification(objectif_a_modif)
        if data_modif:
            ancien_montant = objectif_a_modif.montant_actuel
            nouveau_montant = data_modif["montant_actuel"]
            ecart = nouveau_montant - ancien_montant
            objectif_a_modif.nom = data_modif["nom"]
            objectif_a_modif.montant_objectif = data_modif["montant_objectif"]
            objectif_a_modif.montant_actuel = nouveau_montant
            service.mettre_a_jour_objectif(objectif_a_modif)
            if ecart != 0:
                service.ajouter_transaction(obj_id, ecart)
            st.session_state["mode_modif"] = False
            st.session_state["objectif_a_modifier"] = None
            st.rerun()

# Liste des objectifs
liste_objectifs = service.lister_objectifs()
st.subheader("Vos objectifs d’épargne")
if len(liste_objectifs) == 0:
    st.info("Aucun objectif pour le moment.")
else:
    for obj in liste_objectifs:
        st.write(f"**{obj.nom}** – objectif : **{obj.montant_objectif:.2f} €** | épargné : **{obj.montant_actuel:.2f} €**")
        if obj.montant_objectif > 0:
            progression = min(obj.montant_actuel / obj.montant_objectif, 1.0)
            st.progress(progression)
        col1, col2 = st.columns([1, 1])
        if col1.button("Modifier", key=f"edit_{obj.id}"):
            st.session_state["mode_modif"] = True
            st.session_state["objectif_a_modifier"] = obj.id
            st.rerun()
        if col2.button("Supprimer", key=f"del_{obj.id}"):
            service.supprimer_objectif(obj.id)
            st.rerun()

# Historique des transactions
st.subheader("📜 Historique des transactions")
df_trx = pd.read_sql_query("""
    SELECT t.date, t.montant, o.nom AS objectif
    FROM transactions t
    JOIN objectifs o ON o.id = t.objectif_id
    ORDER BY t.date DESC
""", conn)

if df_trx.empty:
    st.info("Aucune transaction enregistrée pour le moment.")
else:
    df_trx["date"] = pd.to_datetime(df_trx["date"]).dt.strftime("%d/%m/%Y")
    st.dataframe(df_trx, use_container_width=True)


# Données brutes
with st.expander("📊 Afficher les données brutes (base SQLite)"):
    conn = sqlite3.connect("objectifs.db")
    df = pd.read_sql_query("SELECT * FROM objectifs", conn)
    st.dataframe(df)
    conn.close()
