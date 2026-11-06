# REPRISE — où on en est

**Dernière session : 2026-11-06** — commit « Squelette initial de DBMDofus » (premier commit de main).

## État
- Squelette complet et testé (21 tests verts, 1 ignoré faute de captures) : chargeur de boss YAML,
  machine à états du combat (priorité manuelle), alertes avec préavis, overlay PySide6 transparent
  et traversant, raccourcis globaux, capture mss par zone, interface OCR avec confiance.
- Un seul boss : `exemple` (fictif, sert de modèle).
- **Aucun moteur OCR branché** : l'appli tourne en saisie manuelle seule (la boucle de capture ne démarre pas).
- Graphe : 191 nœuds, 385 arêtes, 10 communautés. God nodes : EtatCombat, Application, Overlay.

## Prochaines étapes (dans l'ordre)
1. Premier lancement sur le PC Windows : vérifier overlay, transparence aux clics, raccourcis.
2. Fournir 3-5 captures d'écran Dofus 3 en combat (pleine résolution) → `tests/fixtures/` ; repérer
   où s'affiche le numéro de tour et calibrer `Config.zones["tour"]`.
3. Choisir et brancher le moteur OCR (candidat : RapidOCR) derrière `MoteurOCR`, tests sur les fixtures,
   mesures ms/image et CPU.
4. Premier vrai boss : **Gigalodon** (raid de guilde, 3 tours, déterministe), voir la note du projet
   `claude/boss-mvp-recherche.md`. Il faudra ajouter au modèle la 2ᵉ action du boss à mi-tour
   (quand la moitié des personnages a joué) et une alerte de décision (glyphe noir).
5. Plus tard : config utilisateur persistante (zones, raccourcis), sons d'alerte, déplacement de l'overlay.
