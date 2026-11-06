"""Réglages par défaut : zones d'écran, fréquence de capture, raccourcis.

Les zones sont en pixels écran (x, y, largeur, hauteur). Elles seront
calibrées par l'utilisateur ; ces valeurs ne sont que des points de départ.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_BOSSES = RACINE / "bosses"


@dataclass
class Config:
    # Fréquence de la boucle de capture (images par seconde). Garde-fou CPU.
    fps: float = 2.0
    # Seuil de confiance minimal pour qu'une lecture OCR modifie l'état.
    seuil_confiance: float = 0.80
    # Zones analysées (jamais l'écran entier).
    zones: dict[str, tuple[int, int, int, int]] = field(
        default_factory=lambda: {"tour": (1700, 40, 180, 40)}
    )
    # Raccourcis globaux (format pynput) -> action.
    raccourcis: dict[str, str] = field(
        default_factory=lambda: {
            "<ctrl>+<alt>+d": "debut_combat",
            "<ctrl>+<alt>+f": "fin_combat",
            "<ctrl>+<alt>+n": "tour_suivant",
            "<ctrl>+<alt>+b": "tour_precedent",
            "<ctrl>+<alt>+p": "phase_suivante",
            "<ctrl>+<alt>+m": "boss_suivant",
        }
    )
    # Position de l'overlay (coin haut-gauche) et largeur.
    overlay_pos: tuple[int, int] = (40, 120)
    overlay_largeur: int = 340
