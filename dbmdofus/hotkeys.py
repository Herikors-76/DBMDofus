"""Raccourcis globaux (saisie manuelle). Écoute le clavier, n'envoie rien au jeu.

pynput tourne dans son propre thread : les actions sont relayées au thread
Qt via un signal pour ne jamais toucher l'interface hors du thread principal.
"""
from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal

log = logging.getLogger(__name__)


class Raccourcis(QObject):
    action = Signal(str)

    def __init__(self, correspondances: dict[str, str]):
        super().__init__()
        self.correspondances = dict(correspondances)
        self._ecouteur = None

    def demarrer(self) -> bool:
        try:
            from pynput import keyboard
        except Exception as e:  # pynput absent ou pas d'affichage
            log.warning("Raccourcis globaux indisponibles : %s", e)
            return False
        rappels = {combo: (lambda a=act: self.action.emit(a))
                   for combo, act in self.correspondances.items()}
        self._ecouteur = keyboard.GlobalHotKeys(rappels)
        self._ecouteur.daemon = True
        self._ecouteur.start()
        return True

    def arreter(self) -> None:
        if self._ecouteur is not None:
            self._ecouteur.stop()
            self._ecouteur = None
