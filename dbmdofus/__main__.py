"""Point d'entrée : python -m dbmdofus [--boss ID] [--apercu fichier.png]"""
from __future__ import annotations

import argparse
import logging
import sys

from . import __version__
from .boss_loader import charger_tous
from .config import DOSSIER_BOSSES, Config


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="dbmdofus", description="Alertes de boss pour Dofus 3")
    ap.add_argument("--boss", help="identifiant du boss à charger au démarrage")
    ap.add_argument("--apercu", metavar="PNG",
                    help="rend l'overlay (combat simulé, tour 3) dans une image puis quitte")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s : %(message)s")
    log = logging.getLogger("dbmdofus")

    from PySide6.QtWidgets import QApplication
    from .app import Application

    qapp = QApplication.instance() or QApplication(sys.argv)
    config = Config()
    bosses = charger_tous(DOSSIER_BOSSES)
    log.info("DBMDofus %s — %d boss chargé(s) : %s", __version__, len(bosses),
             ", ".join(b.nom for b in bosses) or "aucun")

    app = Application(config, bosses)
    if args.boss:
        choix = next((b for b in bosses if b.id == args.boss), None)
        if choix is None:
            log.error("Boss inconnu : %s", args.boss)
            return 2
        app.etat.changer_boss(choix)

    if args.apercu:
        app.etat.tour_manuel(3)
        app.rafraichir()
        app.overlay.grab().save(args.apercu)
        log.info("Aperçu enregistré : %s", args.apercu)
        return 0

    app.demarrer()
    log.info("Overlay affiché. Raccourcis : %s", ", ".join(f"{k}={v}" for k, v in config.raccourcis.items()))
    code = qapp.exec()
    app.arreter()
    return code


if __name__ == "__main__":
    sys.exit(main())
