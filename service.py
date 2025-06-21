# service.py
import sqlite3
from models import ObjectifEpargne
import datetime

# Nom du fichier de base de données SQLite
DB_PATH = "objectifs.db"

def init_db():
    """Initialise la base de données SQLite et crée les tables si nécessaire."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table des objectifs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS objectifs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            montant_objectif REAL NOT NULL,
            montant_actuel REAL NOT NULL
        )
    """)

    # Nouvelle table des transactions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            objectif_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            montant REAL NOT NULL,
            FOREIGN KEY(objectif_id) REFERENCES objectifs(id)
        )
    """)

    conn.commit()

    # Insérer quelques données d'exemple si la table est vide
    cursor.execute("SELECT COUNT(*) FROM objectifs")
    count = cursor.fetchone()[0]
    if count == 0:
        exemples = [
            ("Vacances", 2000.0, 150.0),
            ("Achat voiture", 10000.0, 5000.0),
            ("Urgences", 500.0, 500.0)
        ]
        for nom, cible, actuel in exemples:
            cursor.execute(
                "INSERT INTO objectifs (nom, montant_objectif, montant_actuel) VALUES (?, ?, ?)",
                (nom, cible, actuel)
            )
        conn.commit()
    conn.close()

def ajouter_objectif(obj: ObjectifEpargne) -> ObjectifEpargne:
    """Ajoute un nouvel objectif d'épargne dans la base et retourne l'objet avec son ID mis à jour."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO objectifs (nom, montant_objectif, montant_actuel) VALUES (?, ?, ?)",
        (obj.nom, obj.montant_objectif, obj.montant_actuel)
    )
    conn.commit()
    obj.id = cursor.lastrowid
    conn.close()
    return obj

def ajouter_transaction(objectif_id: int, montant: float, date: str = None) -> None:
    """Ajoute une transaction liée à un objectif dans la table transactions."""
    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (objectif_id, date, montant) VALUES (?, ?, ?)",
        (objectif_id, date, montant)
    )
    conn.commit()
    conn.close()

def lister_objectifs() -> list[ObjectifEpargne]:
    """Récupère la liste de tous les objectifs d'épargne stockés en base."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, montant_objectif, montant_actuel FROM objectifs")
    lignes = cursor.fetchall()
    conn.close()
    objectifs = [ObjectifEpargne(id=row[0], nom=row[1],
                                 montant_objectif=row[2], montant_actuel=row[3])
                 for row in lignes]
    return objectifs

def get_objectif(id_obj: int) -> ObjectifEpargne | None:
    """Retourne l'objectif d'épargne ayant l'ID donné, ou None s'il n'existe pas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, montant_objectif, montant_actuel FROM objectifs WHERE id=?", (id_obj,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return ObjectifEpargne(id=row[0], nom=row[1],
                               montant_objectif=row[2], montant_actuel=row[3])
    else:
        return None

def mettre_a_jour_objectif(obj: ObjectifEpargne) -> None:
    """Met à jour un objectif existant (identifié par son id) dans la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE objectifs SET nom=?, montant_objectif=?, montant_actuel=? WHERE id=?",
        (obj.nom, obj.montant_objectif, obj.montant_actuel, obj.id)
    )
    conn.commit()
    conn.close()

def supprimer_objectif(id_obj: int) -> None:
    """Supprime l'objectif d'épargne dont l'id est donné."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM objectifs WHERE id=?", (id_obj,))
    conn.commit()
    conn.close()