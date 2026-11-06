"""Overlay transparent, toujours au premier plan, que les clics traversent."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from . import theme
from .alerts import Alerte
from .combat_state import EtatCombat, Source


class Overlay(QWidget):
    def __init__(self, largeur: int = 340, traversant: bool = True):
        super().__init__()
        drapeaux = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        if traversant:
            drapeaux |= Qt.WindowTransparentForInput
        self.setWindowFlags(drapeaux)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFixedWidth(largeur)
        self.setWindowTitle("DBMDofus")

        police = QFont(theme.POLICE, theme.TAILLE_POLICE)
        self.titre = self._label(theme.OR, police, gras=True)
        self.statut = self._label(theme.TEXTE, police)
        self.alertes = QVBoxLayout()
        self.alertes.setSpacing(2)
        self._police = police

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.addWidget(self.titre)
        lay.addWidget(self.statut)
        lay.addLayout(self.alertes)

    def _label(self, couleur: str, police: QFont, gras: bool = False) -> QLabel:
        l = QLabel()
        f = QFont(police)
        f.setBold(gras)
        l.setFont(f)
        l.setWordWrap(True)
        l.setStyleSheet(f"color: {couleur};")
        return l

    def rafraichir(self, etat: EtatCombat, alertes: list[Alerte]) -> None:
        self.titre.setText(etat.boss.nom if etat.boss else "Aucun boss chargé")
        if not etat.en_combat:
            self.statut.setText("Hors combat — Ctrl+Alt+D pour commencer")
            self.statut.setStyleSheet(f"color: {theme.TEXTE_DISCRET};")
        else:
            phase = etat.boss.phase(etat.phase_id) if etat.boss and etat.phase_id else None
            src = "manuel" if etat.source_tour is Source.MANUEL else f"ocr {etat.confiance:.0%}"
            self.statut.setText(f"Tour {etat.tour} · {phase.nom if phase else '—'}  ({src})")
            self.statut.setStyleSheet(f"color: {theme.TEXTE};")
        while self.alertes.count():
            w = self.alertes.takeAt(0).widget()
            if w:
                w.deleteLater()
        for a in alertes:
            self.alertes.addWidget(self._label(theme.couleur_niveau(a.niveau), self._police,
                                               gras=a.dans_tours == 0))
            self.alertes.itemAt(self.alertes.count() - 1).widget().setText(a.libelle)
        self.adjustSize()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        fond = QColor(theme.NUIT)
        fond.setAlpha(theme.NUIT_ALPHA)
        p.setBrush(fond)
        bord = QColor(theme.OR)
        bord.setAlpha(90)
        p.setPen(bord)
        p.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 10, 10)
