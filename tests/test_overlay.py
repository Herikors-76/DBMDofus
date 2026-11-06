from dbmdofus.alerts import alertes_courantes
from dbmdofus.boss_loader import charger_tous
from dbmdofus.combat_state import EtatCombat
from dbmdofus.config import DOSSIER_BOSSES
from dbmdofus.overlay import Overlay


def test_overlay_rendu(qapp, tmp_path):
    etat = EtatCombat(boss=charger_tous(DOSSIER_BOSSES)[0])
    o = Overlay()
    o.rafraichir(etat, [])
    assert "Hors combat" in o.statut.text()
    etat.tour_manuel(3)
    o.rafraichir(etat, alertes_courantes(etat))
    assert "Tour 3" in o.statut.text()
    assert o.alertes.count() >= 1
    assert o.grab().save(str(tmp_path / "apercu.png"))
