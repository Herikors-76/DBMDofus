"""Vérifie les fiches de référence bosses/reference/*.yaml (relevé des mécaniques, pas des modules
chargés par l'appli) : YAML valide, champs obligatoires, id = nom de fichier, couverture de l'index
des donjons. Code de sortie 1 si une erreur bloquante est trouvée."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent
DOSSIER = RACINE / "bosses" / "reference"
INDEX = RACINE / "outils" / "sources" / "index_donjons.tsv"
OBLIGATOIRES = ("id", "nom", "type", "contenu", "fiabilite", "sources")
TYPES = {"donjon", "raid_guilde"}
FIABILITES = {"confirme", "source_unique", "a_verifier"}
NIVEAUX = {"info", "important", "critique", "action"}  # mêmes niveaux que theme.NIVEAUX_ALERTE
# Entrées de l'index sans boss réel (donjon sans boss).
SANS_BOSS = {"fantome_crocodaille"}


def main() -> int:
    erreurs: list[str] = []
    avertissements: list[str] = []
    ids: set[str] = set()
    for chemin in sorted(DOSSIER.glob("*.yaml")):
        try:
            donnees = yaml.safe_load(chemin.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            erreurs.append(f"{chemin.name}: YAML invalide ({exc})")
            continue
        if not isinstance(donnees, dict):
            erreurs.append(f"{chemin.name}: pas un dictionnaire")
            continue
        manquants = [c for c in OBLIGATOIRES if c not in donnees]
        if manquants:
            erreurs.append(f"{chemin.name}: champs manquants {manquants}")
        if donnees.get("id") != chemin.stem:
            erreurs.append(f"{chemin.name}: id '{donnees.get('id')}' ≠ nom de fichier")
        if donnees.get("type") not in TYPES:
            erreurs.append(f"{chemin.name}: type inconnu '{donnees.get('type')}'")
        if donnees.get("fiabilite") not in FIABILITES:
            erreurs.append(f"{chemin.name}: fiabilité inconnue '{donnees.get('fiabilite')}'")
        for alerte in donnees.get("alertes") or []:
            if alerte.get("niveau") not in NIVEAUX:
                erreurs.append(f"{chemin.name}: niveau d'alerte inconnu '{alerte.get('niveau')}'")
            if not alerte.get("texte"):
                erreurs.append(f"{chemin.name}: alerte sans texte")
        if donnees.get("completude") == "a_completer":
            avertissements.append(f"{chemin.name}: fiche à compléter")
        elif not donnees.get("alertes"):
            avertissements.append(f"{chemin.name}: aucune alerte")
        ids.add(chemin.stem)

    with INDEX.open(encoding="utf-8") as f:
        attendus = {ligne["id"] for ligne in csv.DictReader(f, delimiter="\t")} - SANS_BOSS
    for manquant in sorted(attendus - ids):
        erreurs.append(f"index: pas de fiche pour '{manquant}'")

    for message in avertissements:
        print("AVERTISSEMENT", message)
    for message in erreurs:
        print("ERREUR", message)
    print(f"{len(ids)} fiches, {len(erreurs)} erreur(s), {len(avertissements)} avertissement(s)")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
