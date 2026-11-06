"""Chargeur de modules de boss : bosses/<boss>.yaml -> objets Boss validés.

Aucune mécanique n'est écrite dans le code : tout vient des YAML.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .theme import NIVEAUX_ALERTE

log = logging.getLogger(__name__)


class BossInvalide(ValueError):
    """Fichier de boss mal formé."""


@dataclass(frozen=True)
class Phase:
    id: str
    nom: str
    tour_debut: int | None = None  # None = déclenchée à la main


@dataclass(frozen=True)
class Mecanique:
    id: str
    nom: str
    texte: str
    niveau: str = "info"
    tours: tuple[int, ...] = ()      # tours précis
    tous_les: int | None = None      # récurrence
    a_partir_de: int = 1             # premier tour de la récurrence
    phase: str | None = None         # limitée à une phase
    avance: int = 0                  # prévenir N tours avant

    def tombe_au_tour(self, tour: int) -> bool:
        if tour in self.tours:
            return True
        if self.tous_les and tour >= self.a_partir_de:
            return (tour - self.a_partir_de) % self.tous_les == 0
        return False


@dataclass(frozen=True)
class Boss:
    id: str
    nom: str
    phases: tuple[Phase, ...]
    mecaniques: tuple[Mecanique, ...]
    strategie: str = ""
    doc: str = ""
    source: Path | None = field(default=None, compare=False)

    def phase(self, phase_id: str) -> Phase | None:
        return next((p for p in self.phases if p.id == phase_id), None)


def _exiger(d: dict, cle: str, ou: str):
    if cle not in d or d[cle] in (None, ""):
        raise BossInvalide(f"{ou} : champ obligatoire « {cle} » manquant")
    return d[cle]


def boss_depuis_dict(d: dict, source: Path | None = None) -> Boss:
    """Valide un dictionnaire (YAML parsé) et construit un Boss."""
    ou = str(source or "boss")
    if not isinstance(d, dict):
        raise BossInvalide(f"{ou} : le fichier doit contenir un dictionnaire")
    boss_id = _exiger(d, "id", ou)

    phases = []
    for p in d.get("phases") or [{"id": "p1", "nom": "Phase unique", "debut": {"tour": 1}}]:
        debut = p.get("debut") or {}
        phases.append(Phase(_exiger(p, "id", ou), p.get("nom", p["id"]), debut.get("tour")))
    ids_phases = {p.id for p in phases}
    if len(ids_phases) != len(phases):
        raise BossInvalide(f"{ou} : identifiants de phase en double")

    mecas = []
    for m in d.get("mecaniques") or []:
        mid = _exiger(m, "id", ou)
        alerte = m.get("alerte") or {}
        niveau = alerte.get("niveau", "info")
        if niveau not in NIVEAUX_ALERTE:
            raise BossInvalide(f"{ou} / {mid} : niveau « {niveau} » inconnu ({', '.join(NIVEAUX_ALERTE)})")
        phase = m.get("phase")
        if phase and phase not in ids_phases:
            raise BossInvalide(f"{ou} / {mid} : phase « {phase} » inexistante")
        tours = tuple(int(t) for t in m.get("tours") or ())
        tous_les = m.get("tous_les")
        if not tours and not tous_les:
            raise BossInvalide(f"{ou} / {mid} : il faut « tours » ou « tous_les »")
        mecas.append(Mecanique(
            id=mid, nom=m.get("nom", mid), texte=_exiger(alerte, "texte", f"{ou} / {mid}"),
            niveau=niveau, tours=tours, tous_les=int(tous_les) if tous_les else None,
            a_partir_de=int(m.get("a_partir_de", 1)), phase=phase,
            avance=int(alerte.get("avance", 0)),
        ))
    return Boss(boss_id, d.get("nom", boss_id), tuple(phases), tuple(mecas),
                d.get("strategie", "") or "", d.get("doc", "") or "", source)


def charger_boss(chemin: Path) -> Boss:
    with open(chemin, encoding="utf-8") as f:
        return boss_depuis_dict(yaml.safe_load(f), chemin)


def charger_tous(dossier: Path) -> list[Boss]:
    """Charge tous les bosses/*.yaml ; un fichier invalide est signalé et ignoré."""
    bosses = []
    for chemin in sorted(Path(dossier).glob("*.yaml")):
        try:
            bosses.append(charger_boss(chemin))
        except (BossInvalide, yaml.YAMLError) as e:
            log.error("Boss ignoré : %s", e)
    return bosses
