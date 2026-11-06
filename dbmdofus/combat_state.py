"""Machine à états du combat : en combat ou non, tour, phase.

Deux sources : OCR (avec confiance) et saisie manuelle (raccourcis).
La saisie manuelle prend toujours le dessus : après une correction à la
main, l'OCR n'est plus écouté que s'il annonce le tour suivant (progression
cohérente), ce qui lève le verrou.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .boss_loader import Boss


class Source(str, Enum):
    MANUEL = "manuel"
    OCR = "ocr"


@dataclass
class EtatCombat:
    boss: Boss | None = None
    seuil_confiance: float = 0.80
    en_combat: bool = False
    tour: int = 0
    phase_id: str | None = None
    source_tour: Source = Source.MANUEL
    confiance: float = 1.0
    _verrou_manuel: bool = False
    _phase_manuelle: bool = False
    journal: list[str] = field(default_factory=list)

    # --- cycle de vie -------------------------------------------------
    def debut_combat(self) -> None:
        self.en_combat, self.tour = True, 1
        self._verrou_manuel = self._phase_manuelle = False
        self.source_tour, self.confiance = Source.MANUEL, 1.0
        self._maj_phase_auto()
        self._noter("début du combat")

    def fin_combat(self) -> None:
        self.en_combat, self.tour, self.phase_id = False, 0, None
        self._noter("fin du combat")

    def changer_boss(self, boss: Boss | None) -> None:
        self.boss = boss
        self.fin_combat()

    # --- saisie manuelle (prioritaire) -------------------------------
    def tour_manuel(self, tour: int) -> None:
        if not self.en_combat:
            self.debut_combat()
        self.tour = max(1, tour)
        self.source_tour, self.confiance = Source.MANUEL, 1.0
        self._verrou_manuel = True
        self._maj_phase_auto()
        self._noter(f"tour {self.tour} (manuel)")

    def tour_suivant(self) -> None:
        self.tour_manuel(self.tour + 1)

    def tour_precedent(self) -> None:
        self.tour_manuel(self.tour - 1)

    def phase_manuelle(self, phase_id: str) -> None:
        if self.boss and self.boss.phase(phase_id):
            self.phase_id, self._phase_manuelle = phase_id, True
            self._noter(f"phase {phase_id} (manuel)")

    def phase_suivante(self) -> None:
        if not self.boss:
            return
        ids = [p.id for p in self.boss.phases]
        i = ids.index(self.phase_id) + 1 if self.phase_id in ids else 0
        self.phase_manuelle(ids[min(i, len(ids) - 1)])

    # --- lectures OCR -------------------------------------------------
    def lecture_tour(self, tour: int, confiance: float) -> bool:
        """Applique une lecture OCR du tour. Renvoie True si l'état a changé."""
        if confiance < self.seuil_confiance or tour < 1:
            return False
        if not self.en_combat:
            self.debut_combat()
        if tour == self.tour:
            return False
        if self._verrou_manuel and tour != self.tour + 1:
            return False  # la saisie manuelle prime
        if tour < self.tour:
            return False  # pas de retour arrière par OCR
        self._verrou_manuel = False
        self.tour, self.source_tour, self.confiance = tour, Source.OCR, confiance
        self._maj_phase_auto()
        self._noter(f"tour {tour} (ocr {confiance:.0%})")
        return True

    # --- interne ------------------------------------------------------
    def _maj_phase_auto(self) -> None:
        if not self.boss or self._phase_manuelle:
            return
        candidates = [p for p in self.boss.phases
                      if p.tour_debut is not None and p.tour_debut <= self.tour]
        if candidates:
            self.phase_id = max(candidates, key=lambda p: p.tour_debut).id
        elif self.phase_id is None:
            self.phase_id = self.boss.phases[0].id

    def _noter(self, msg: str) -> None:
        self.journal.append(msg)
        del self.journal[:-50]
