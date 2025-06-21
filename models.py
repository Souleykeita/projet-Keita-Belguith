# models.py
from dataclasses import dataclass

@dataclass
class ObjectifEpargne:
    """Représentation d'un objectif d'épargne."""
    id: int | None = None               # Identifiant unique (primary key SQLite)
    nom: str = ""                       # Nom de l'objectif (description)
    montant_objectif: float = 0.0       # Montant cible à atteindre en euros
    montant_actuel: float = 0.0         # Montant actuel épargné en euros
