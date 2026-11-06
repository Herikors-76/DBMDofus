<!-- GENERE par outils/generer_docs_reference.py : ne pas éditer, modifier le YAML -->
# Princesse Maudite

Sanctuaire des Jardins éternels (boss final)

Fiche de référence : `bosses/reference/princesse_maudite.yaml` · fiabilité : **source_unique**

## États
- Lourd
- Inérodable
- Invulnérable au corps à corps

## Sorts
- **Appel du Protecteur** : Invoque Dahliane/Tritulipe/Muguégide/Fracamélia ; relance 2 tours
- **Drainfecte** : 650 feu en vol de vie, vole 1 PO 2 tours ; portée 10, 4 fois par tour
- **Florigine** : Fleur chez elle : 1 050 air en vol de vie en croix de taille 4, -3 PA. Fleur chez vous : 10 % d'érosion + 1 050 air ; portée 12
- **Maléfissure** : -1 tour d'envoûtement, 900 terre en étoile de taille 2, poussée de 4 ignorant les états d'immobilisation
- **Purifiction** : Retire Enraciné/Pesanteur/Indéplaçable, +1 PM, échange de place, 400 air ; dès le tour 2
- **Roncitron** : 900 eau en croix de taille 4, attire vers le centre ; portée 12
- **Tempête Florale** : À 10 Floraison : 10 % d'érosion 2 tours, gros dégâts à tous ; en phase 2, +100 % critique 2 tours et soin de 10 000

## Mécaniques
- **Aura Maudite** (début du tour de la Princesse, dès le tour 2) : Les persos dans sa ligne de vue deviennent Statues (passent leur tour) et sont tués au début de son tour suivant ; un coup d'arme sur la statue lève la malédiction
- **Invocations** (tous les 2 tours) : Monstre aléatoire qui la suit
- **Floraison** : 
- **Incantation Florale** : Glyphe sur la bordure centrale quand la Fleur est dans son camp ; qui marche dessus reçoit le sort (2 PA, 10 PO, sans ligne de vue, usage unique). Sur la Princesse 2 fois = fin de l'invulnérabilité ; sur un allié = -1 tour d'envoûtement et bouclier de 200 % du niveau

## Stratégie
- {'Phase 1': "tuer l'invocation, déclencher le seuil de la Fleur, la coincer dans un coin"}
- {'Phase 2': "tuer la Volonté d'abord, puis 2 Incantations sur la Princesse"}
- Hors de sa ligne de vue au début de chacun de ses tours
- Réduction de soins (Leçon de Grunob) contre le soin de Tempête Florale
- Variante autowin : retrait de PM total (2 retraits ≥ 300, Éliotrope, Ouginak/Crâ pour l'esquive, Pandawa placeur en dernier)

## Alertes
- [critique] Aura Maudite : sortez de sa ligne de vue !
- [critique] Floraison 9/10 : Tempête Florale au prochain sort
- [critique] Statue : un coup d'arme pour le libérer
- [info] Invocation : nettoyez

## Sources
- https://www.dofuspourlesnoobs.com/sanctuaire-des-jardins-eternels.html
