from pathlib import Path

import pytest

from dbmdofus.boss_loader import BossInvalide, boss_depuis_dict, charger_tous
from dbmdofus.config import DOSSIER_BOSSES, RACINE


def test_tous_les_boss_sont_valides_et_documentes():
    fichiers = sorted(DOSSIER_BOSSES.glob("*.yaml"))
    bosses = charger_tous(DOSSIER_BOSSES)
    assert len(bosses) == len(fichiers) > 0  # aucun fichier ignoré
    for b in bosses:
        assert b.doc == f"docs/bosses/{b.id}.md"
        assert (RACINE / b.doc).is_file(), f"doc manquante pour {b.id}"
    assert len({b.id for b in bosses}) == len(bosses)


def test_recurrence():
    b = boss_depuis_dict({"id": "x", "mecaniques": [
        {"id": "m", "tous_les": 3, "a_partir_de": 3, "alerte": {"texte": "t"}}]})
    m = b.mecaniques[0]
    assert [t for t in range(1, 11) if m.tombe_au_tour(t)] == [3, 6, 9]


@pytest.mark.parametrize("meca", [
    {"id": "m", "tours": [1], "alerte": {"texte": "t", "niveau": "inconnu"}},
    {"id": "m", "tours": [1], "phase": "absente", "alerte": {"texte": "t"}},
    {"id": "m", "alerte": {"texte": "t"}},
    {"id": "m", "tours": [1], "alerte": {}},
])
def test_boss_invalides(meca):
    with pytest.raises(BossInvalide):
        boss_depuis_dict({"id": "x", "mecaniques": [meca]})


def test_fichier_invalide_ignore(tmp_path: Path):
    (tmp_path / "ok.yaml").write_text("id: ok\n", encoding="utf-8")
    (tmp_path / "ko.yaml").write_text("nom: sans id\n", encoding="utf-8")
    assert [b.id for b in charger_tous(tmp_path)] == ["ok"]
