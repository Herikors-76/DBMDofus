"""Règles du projet vérifiées automatiquement."""
import re
from pathlib import Path

PAQUET = Path(__file__).resolve().parent.parent / "dbmdofus"
COULEUR = re.compile(r"#[0-9a-fA-F]{6}\b|rgba?\(")
INTERDITS = re.compile(r"\b(pymem|ReadProcessMemory|pydivert|scapy|pyautogui|SendInput)\b")


def test_aucune_couleur_en_dur_hors_theme():
    for f in PAQUET.rglob("*.py"):
        if f.name != "theme.py":
            assert not COULEUR.search(f.read_text(encoding="utf-8")), f"couleur en dur dans {f.name}"


def test_cgu_pas_de_memoire_paquets_ni_actions():
    for f in PAQUET.rglob("*.py"):
        assert not INTERDITS.search(f.read_text(encoding="utf-8")), f"API interdite dans {f.name}"
