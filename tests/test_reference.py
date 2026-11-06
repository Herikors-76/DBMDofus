"""Fiches de référence (bosses/reference/) : valides, documentées, invisibles pour le chargeur."""
import subprocess
import sys

from dbmdofus.boss_loader import charger_tous
from dbmdofus.config import DOSSIER_BOSSES, RACINE

REFERENCE = DOSSIER_BOSSES / "reference"


def test_fiches_reference_valides():
    resultat = subprocess.run(
        [sys.executable, str(RACINE / "outils" / "valider_reference.py")],
        capture_output=True, text=True,
    )
    assert resultat.returncode == 0, resultat.stdout


def test_chaque_fiche_a_sa_doc():
    ids = {p.stem for p in REFERENCE.glob("*.yaml")}
    docs = {p.stem for p in (RACINE / "docs" / "bosses" / "reference").glob("*.md")}
    assert ids and ids <= docs, f"docs manquantes : {sorted(ids - docs)}"


def test_reference_non_chargee_comme_module():
    ids_modules = {b.id for b in charger_tous(DOSSIER_BOSSES)}
    assert "nileza" not in ids_modules  # fiche de référence seulement
    assert "gigalodon" in ids_modules   # module réel
