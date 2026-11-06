# REPRISE — où on en est

**Dernière session : 2026-11-06** — commit « Données : Gigalodon en module + 131 fiches de référence ».

## État
- Squelette complet et testé (24 tests verts, 1 ignoré faute de captures) : chargeur de boss YAML,
  machine à états du combat (priorité manuelle), alertes avec préavis, overlay PySide6 transparent
  et traversant, raccourcis globaux, capture mss par zone, interface OCR avec confiance.
- Modules chargés : `exemple` (fictif) et **`gigalodon`** (premier vrai boss, alertes par tour).
- Relevé de **131 boss** dans `bosses/reference/` (10 de raid de guilde, 121 de donjon, niveaux 10 à 200),
  non chargés par l'appli : ce sont la matière pour écrire les futurs modules.
- **Aucun moteur OCR branché** : l'appli tourne en saisie manuelle seule (la boucle de capture ne démarre pas).
- Graphe : 236 nœuds, 441 arêtes, 10 communautés. God nodes : EtatCombat, Application, Overlay
  (fiches de référence exclues du graphe).

## Prochaines étapes (dans l'ordre)
1. Premier lancement sur le PC Windows : vérifier overlay, transparence aux clics, raccourcis.
2. Fournir 3-5 captures d'écran Dofus 3 en combat (pleine résolution) → `tests/fixtures/` ; repérer
   où s'affiche le numéro de tour et calibrer `Config.zones["tour"]`. Priorité : combat du Gigalodon
   (compteur de tours sur la machine au bord de la map, glyphe noir).
3. Choisir et brancher le moteur OCR (candidat : RapidOCR) derrière `MoteurOCR`, tests sur les fixtures,
   mesures ms/image et CPU.
4. Modèle : ajouter un déclencheur « mi-tour » (2ᵉ action du Gigalodon, Défenseur, Reine Écarlate,
   Princesse Maudite) et des alertes sur seuils de PV / états ; aujourd'hui `gigalodon.yaml` les annonce
   à chaque tour faute de mieux.
5. Overlay : gérer les retours à la ligne des alertes longues (aujourd'hui les lignes se chevauchent ;
   contourné en gardant les textes ≈ 35 caractères).
6. Convertir d'autres fiches de référence en modules (raids d'abord), compléter `servitude` et
   `corruption`, vérifier en jeu les fiches `a_verifier`.
7. Plus tard : config utilisateur persistante (zones, raccourcis), sons d'alerte, déplacement de l'overlay.
