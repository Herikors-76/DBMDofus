"""Thème « nuit aux lucioles » : SEUL fichier où des couleurs sont écrites.

Règle : or pour mettre en valeur, vert pour agir. Tout le reste du code
importe ces constantes (un test vérifie l'absence de couleur en dur ailleurs).
"""

# Couleurs de base
OR = "#f4c260"          # mise en valeur (boss, tour, titres)
VERT = "#89b820"        # agir (alerte « à faire maintenant »)
NUIT = "#0e1424"        # fond
NUIT_ALPHA = 200        # opacité du fond de l'overlay (0-255)
TEXTE = "#e8e4d8"       # texte courant
TEXTE_DISCRET = "#8a8fa3"
ROUGE_BRAISE = "#e0563b"  # danger critique

# Couleur par niveau d'alerte (clé = valeur `niveau` des YAML de boss)
NIVEAUX_ALERTE = {
    "info": TEXTE,
    "important": OR,
    "critique": ROUGE_BRAISE,
    "action": VERT,
}

POLICE = "Segoe UI"
TAILLE_POLICE = 11


def couleur_niveau(niveau: str) -> str:
    """Couleur d'un niveau d'alerte, TEXTE si niveau inconnu."""
    return NIVEAUX_ALERTE.get(niveau, TEXTE)
