# ETAT — journal daté

## 2026-11-06 — Données de boss
- Module `bosses/gigalodon.yaml` + doc manuelle : 6 mécaniques (placement, double jeu, glyphe noir,
  plan de burst, dernier tour en `action` avec préavis). Aperçu de l'overlay vérifié au tour 3.
- `bosses/reference/` : 131 fiches (10 boss de raid : Gouffre du Gigalodon et Sanctuaire des Jardins
  éternels ; 121 boss de donjon), 435 sorts, 208 alertes. Fiabilité : 1 confirmée, 125 source unique,
  5 à vérifier ; 2 à compléter (Servitude, Corruption). Docs générées dans `docs/bosses/reference/`.
- Outils : `valider_reference.py`, `generer_docs_reference.py`, index des 122 donjons.
- pytest : 21 → 24 réussis, 0 échec, 1 ignoré.
- Graphe : 191 → 236 nœuds, 385 → 441 arêtes, 10 communautés ; god nodes inchangés.
- Défaut repéré : l'overlay superpose les alertes trop longues (pas de retour à la ligne).

## 2026-11-06 — Squelette initial
- Création du paquet `dbmdofus/` (11 modules), du boss modèle `exemple`, des tests, de CARTE.md,
  REPRISE.md, `.graphifyignore` et `outils/carte_index.py`.
- pytest : 21 réussis, 0 échec, 1 ignoré (pas encore de captures OCR).
- Rendu de l'overlay vérifié hors écran (`--apercu`) : titre en or, alerte critique en rouge braise.
- Graphe : 0 → 191 nœuds, 385 arêtes, 10 communautés. God nodes : EtatCombat (25), Application (18), Overlay (14).
- Pas de mesure CPU : aucune capture active tant qu'aucun moteur OCR n'est branché.
