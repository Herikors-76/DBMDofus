"""Assemblage : config, boss, état, raccourcis, boucle de capture, overlay."""
from __future__ import annotations

import logging

from PySide6.QtCore import QTimer

from .alerts import alertes_courantes
from .boss_loader import Boss
from .capture import Capture
from .combat_state import EtatCombat
from .config import Config
from .hotkeys import Raccourcis
from .ocr import MoteurAucun, MoteurOCR
from .overlay import Overlay

log = logging.getLogger(__name__)


class Application:
    def __init__(self, config: Config, bosses: list[Boss], moteur: MoteurOCR | None = None,
                 overlay: Overlay | None = None):
        self.config = config
        self.bosses = bosses
        self.moteur = moteur or MoteurAucun()
        self.etat = EtatCombat(boss=bosses[0] if bosses else None,
                               seuil_confiance=config.seuil_confiance)
        self.overlay = overlay or Overlay(config.overlay_largeur)
        self.capture = Capture(config.zones)
        self.raccourcis = Raccourcis(config.raccourcis)
        self.raccourcis.action.connect(self.executer)
        self.minuteur = QTimer()
        self.minuteur.setInterval(int(1000 / max(config.fps, 0.1)))
        self.minuteur.timeout.connect(self.boucle)

    def demarrer(self) -> None:
        self.overlay.move(*self.config.overlay_pos)
        self.rafraichir()
        self.overlay.show()
        self.raccourcis.demarrer()
        if self.moteur.disponible:
            self.minuteur.start()
            log.info("Boucle de capture : %.1f img/s, zones %s", self.config.fps, list(self.config.zones))
        else:
            log.info("Aucun moteur OCR : capture à l'arrêt, saisie manuelle seulement")

    def boucle(self) -> None:
        """Chemin chaud : une capture de zone + une lecture par tick."""
        if not self.etat.en_combat and not self.etat.boss:
            return
        lecture = self.moteur.lire(self.capture.saisir("tour"))
        n = lecture.nombre()
        if n is not None and self.etat.lecture_tour(n, lecture.confiance):
            self.rafraichir()

    def executer(self, action: str) -> None:
        e = self.etat
        actions = {
            "debut_combat": e.debut_combat,
            "fin_combat": e.fin_combat,
            "tour_suivant": e.tour_suivant,
            "tour_precedent": e.tour_precedent,
            "phase_suivante": e.phase_suivante,
            "boss_suivant": self.boss_suivant,
        }
        if action in actions:
            actions[action]()
            self.rafraichir()

    def boss_suivant(self) -> None:
        if not self.bosses:
            return
        i = self.bosses.index(self.etat.boss) + 1 if self.etat.boss in self.bosses else 0
        self.etat.changer_boss(self.bosses[i % len(self.bosses)])
        log.info("Boss : %s", self.etat.boss.nom)

    def rafraichir(self) -> None:
        self.overlay.rafraichir(self.etat, alertes_courantes(self.etat))

    def arreter(self) -> None:
        self.minuteur.stop()
        self.raccourcis.arreter()
        self.capture.fermer()
