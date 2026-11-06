"""Calcul des alertes à afficher pour le tour et la phase courants."""
from __future__ import annotations

from dataclasses import dataclass

from .combat_state import EtatCombat


@dataclass(frozen=True)
class Alerte:
    texte: str
    niveau: str
    dans_tours: int  # 0 = ce tour-ci

    @property
    def libelle(self) -> str:
        if self.dans_tours == 0:
            return f"MAINTENANT : {self.texte}"
        return f"Dans {self.dans_tours} tour{'s' if self.dans_tours > 1 else ''} : {self.texte}"


def alertes_courantes(etat: EtatCombat) -> list[Alerte]:
    """Alertes du tour courant et préavis (champ `avance` des mécaniques)."""
    if not etat.en_combat or not etat.boss:
        return []
    res = []
    for m in etat.boss.mecaniques:
        if m.phase and m.phase != etat.phase_id:
            continue
        for d in range(0, m.avance + 1):
            if m.tombe_au_tour(etat.tour + d):
                res.append(Alerte(m.texte, "action" if d == 0 and m.niveau == "info" else m.niveau, d))
                break
    res.sort(key=lambda a: a.dans_tours)
    return res
