import pytest

from dbmdofus.alerts import alertes_courantes
from dbmdofus.boss_loader import charger_boss
from dbmdofus.combat_state import EtatCombat, Source
from dbmdofus.config import DOSSIER_BOSSES


@pytest.fixture
def etat():
    return EtatCombat(boss=charger_boss(DOSSIER_BOSSES / "exemple.yaml"), seuil_confiance=0.8)


def test_ocr_faible_confiance_ignoree(etat):
    etat.debut_combat()
    assert not etat.lecture_tour(2, 0.5)
    assert etat.tour == 1


def test_ocr_accepte_et_phase_auto(etat):
    etat.debut_combat()
    assert etat.lecture_tour(6, 0.95)
    assert etat.source_tour is Source.OCR and etat.phase_id == "p2"


def test_ocr_ne_recule_pas(etat):
    etat.debut_combat()
    etat.lecture_tour(5, 0.9)
    assert not etat.lecture_tour(4, 0.99)


def test_manuel_prend_le_dessus(etat):
    etat.debut_combat()
    etat.lecture_tour(4, 0.9)
    etat.tour_manuel(2)                     # correction à la main
    assert not etat.lecture_tour(4, 0.99)   # l'OCR contredit : ignoré
    assert etat.tour == 2
    assert etat.lecture_tour(3, 0.9)        # progression cohérente : verrou levé
    assert etat.lecture_tour(5, 0.9)


def test_phase_manuelle_bloque_phase_auto(etat):
    etat.debut_combat()
    etat.phase_manuelle("p3")
    etat.tour_manuel(7)
    assert etat.phase_id == "p3"


def test_alertes_et_preavis(etat):
    etat.debut_combat()
    etat.tour_manuel(2)
    libelles = [a.libelle for a in alertes_courantes(etat)]
    assert libelles[0].startswith("MAINTENANT : Bouclier")
    assert any(l.startswith("Dans 1 tour : Onde") for l in libelles)


def test_pas_alerte_hors_combat(etat):
    assert alertes_courantes(etat) == []
