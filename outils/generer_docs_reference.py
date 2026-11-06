"""Génère docs/bosses/reference/<id>.md à partir de bosses/reference/<id>.yaml.
Une doc écrite à la main (sans l'en-tête GENERE) n'est jamais écrasée."""
from __future__ import annotations

from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "bosses" / "reference"
CIBLE = RACINE / "docs" / "bosses" / "reference"
GENERE = "<!-- GENERE par outils/generer_docs_reference.py : ne pas éditer, modifier le YAML -->"


def _liste(titre: str, elements, rendu) -> list[str]:
    if not elements:
        return []
    return [f"## {titre}", *[f"- {rendu(e)}" for e in elements], ""]


def rendre(d: dict) -> str:
    lignes = [GENERE, f"# {d['nom']}", ""]
    infos = [d["contenu"]]
    if d.get("niveau") is not None:
        infos.append(f"niveau {d['niveau']}")
    if d.get("position"):
        infos.append(f"position [{d['position']}]")
    if d.get("pv") is not None:
        infos.append(f"PV {d['pv']}")
    lignes += [" · ".join(str(i) for i in infos), "",
               f"Fiche de référence : `bosses/reference/{d['id']}.yaml` · fiabilité : **{d['fiabilite']}**", ""]
    if d.get("completude") == "a_completer":
        lignes += ["> ⚠️ Fiche à compléter : mécaniques non relevées.", ""]
    lignes += _liste("États", d.get("etats") or d.get("etats_initiaux") or d.get("etats_permanents"), str)
    lignes += _liste("Sorts", d.get("sorts"), lambda s: f"**{s['nom']}** : {s.get('effet', '')}")
    lignes += _liste("Mécaniques", d.get("mecaniques") or d.get("passifs"),
                     lambda m: f"**{m['nom']}**" + (f" ({m['declencheur']})" if m.get("declencheur") else "")
                     + f" : {m.get('effet', '')}")
    lignes += _liste("Stratégie", d.get("strategie"), str)
    lignes += _liste("Alertes", d.get("alertes"), lambda a: f"[{a['niveau']}] {a['texte']}")
    lignes += _liste("Sources", d.get("sources"), str)
    return "\n".join(lignes).rstrip() + "\n"


def main() -> None:
    CIBLE.mkdir(parents=True, exist_ok=True)
    ecrits = ignores = 0
    for chemin in sorted(SOURCE.glob("*.yaml")):
        d = yaml.safe_load(chemin.read_text(encoding="utf-8"))
        doc = CIBLE / f"{d['id']}.md"
        if doc.exists() and not doc.read_text(encoding="utf-8").startswith(GENERE):
            ignores += 1
            continue
        doc.write_text(rendre(d), encoding="utf-8")
        ecrits += 1
    print(f"{ecrits} docs générées, {ignores} docs manuelles conservées")


if __name__ == "__main__":
    main()
