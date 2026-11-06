"""Régénère l'index automatique de CARTE.md (entre les balises INDEX).

Usage : python outils/carte_index.py
Liste, pour chaque module Python : sa première ligne de docstring, ses
classes et fonctions de premier niveau avec numéro de ligne ; puis les boss.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent
CARTE = RACINE / "CARTE.md"
DEBUT, FIN = "<!-- INDEX:DEBUT -->", "<!-- INDEX:FIN -->"
DOSSIERS = ["dbmdofus", "outils", "tests"]


def _resume(noeud) -> str:
    doc = ast.get_docstring(noeud)
    return doc.strip().splitlines()[0] if doc else ""


def index_module(chemin: Path) -> list[str]:
    arbre = ast.parse(chemin.read_text(encoding="utf-8"))
    rel = chemin.relative_to(RACINE).as_posix()
    lignes = [f"- `{rel}` — {_resume(arbre)}".rstrip(" —")]
    for n in arbre.body:
        if isinstance(n, ast.ClassDef):
            methodes = [m.name for m in n.body
                        if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)) and not m.name.startswith("__")]
            suite = f" : {', '.join(methodes)}" if methodes else ""
            lignes.append(f"  - classe `{n.name}` (l.{n.lineno}){suite}")
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            lignes.append(f"  - `{n.name}()` (l.{n.lineno})")
    return lignes


def index_bosses() -> list[str]:
    lignes = []
    for f in sorted((RACINE / "bosses").glob("*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        lignes.append(f"- `bosses/{f.name}` — {d.get('nom', '?')} : "
                      f"{len(d.get('phases') or [])} phase(s), {len(d.get('mecaniques') or [])} mécanique(s), "
                      f"doc `{d.get('doc', '—')}`")
    return lignes or ["- (aucun)"]


def generer() -> str:
    out = ["### Modules"]
    for dossier in DOSSIERS:
        for f in sorted((RACINE / dossier).rglob("*.py")):
            if "__pycache__" not in f.parts:
                out += index_module(f)
    out += ["", "### Boss"] + index_bosses()
    return "\n".join(out)


def main() -> int:
    texte = CARTE.read_text(encoding="utf-8")
    if DEBUT not in texte or FIN not in texte:
        print("Balises INDEX absentes de CARTE.md", file=sys.stderr)
        return 1
    avant, reste = texte.split(DEBUT, 1)
    _, apres = reste.split(FIN, 1)
    CARTE.write_text(f"{avant}{DEBUT}\n{generer()}\n{FIN}{apres}", encoding="utf-8")
    print("CARTE.md : index mis à jour")
    return 0


if __name__ == "__main__":
    sys.exit(main())
