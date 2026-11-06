"""Lecture d'images : OCR et détection de motifs, toujours avec confiance.

Le moteur OCR est enfichable (protocole MoteurOCR). Tant qu'aucun moteur
n'est choisi, MoteurAucun renvoie une confiance nulle et la boucle de
capture reste à l'arrêt : seule la saisie manuelle pilote l'état.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol

import cv2
import numpy as np


@dataclass(frozen=True)
class Lecture:
    valeur: str
    confiance: float  # 0.0 à 1.0

    def nombre(self) -> int | None:
        m = re.search(r"\d+", self.valeur)
        return int(m.group()) if m else None


class MoteurOCR(Protocol):
    disponible: bool

    def lire(self, image: np.ndarray) -> Lecture: ...


class MoteurAucun:
    """Aucun moteur installé : ne lit rien."""
    disponible = False

    def lire(self, image: np.ndarray) -> Lecture:
        return Lecture("", 0.0)


def preparer(image: np.ndarray, echelle: float = 2.0) -> np.ndarray:
    """Niveaux de gris + agrandissement + binarisation (Otsu) avant OCR."""
    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    if echelle != 1.0:
        gris = cv2.resize(gris, None, fx=echelle, fy=echelle, interpolation=cv2.INTER_CUBIC)
    _, binaire = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binaire


def detecter_motif(image: np.ndarray, motif: np.ndarray) -> Lecture:
    """Cherche un motif (icône, bandeau) ; valeur = « x,y », confiance = score."""
    if image.shape[0] < motif.shape[0] or image.shape[1] < motif.shape[1]:
        return Lecture("", 0.0)
    res = cv2.matchTemplate(image, motif, cv2.TM_CCOEFF_NORMED)
    _, score, _, (x, y) = cv2.minMaxLoc(res)
    return Lecture(f"{x},{y}", max(0.0, float(score)))
