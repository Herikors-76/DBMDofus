"""Capture d'écran limitée aux zones utiles (mss). Chemin chaud.

Garde-fous : jamais l'écran entier, mss créé une seule fois, temps de
capture mesuré (ms par image) pour suivre la cible < 5 % CPU.
"""
from __future__ import annotations

import time

import numpy as np


class Capture:
    def __init__(self, zones: dict[str, tuple[int, int, int, int]]):
        self.zones = dict(zones)
        self._sct = None
        self.ms_derniere = 0.0
        self.ms_moyenne = 0.0

    def _mss(self):
        if self._sct is None:
            import mss  # import tardif : pas d'écran requis pour les tests
            self._sct = mss.mss()
        return self._sct

    def saisir(self, nom_zone: str) -> np.ndarray:
        """Image BGR (numpy) de la zone demandée."""
        x, y, w, h = self.zones[nom_zone]
        t0 = time.perf_counter()
        brut = self._mss().grab({"left": x, "top": y, "width": w, "height": h})
        img = np.asarray(brut)[:, :, :3]  # BGRA -> BGR, sans copie
        self.ms_derniere = (time.perf_counter() - t0) * 1000
        self.ms_moyenne = 0.9 * self.ms_moyenne + 0.1 * self.ms_derniere if self.ms_moyenne else self.ms_derniere
        return img

    def fermer(self) -> None:
        if self._sct is not None:
            self._sct.close()
            self._sct = None
