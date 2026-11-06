# Gigalodon

Boss final du raid de guilde **Gouffre du Gigalodon** (màj 3.6, niveau 200, 8 à 12 joueurs).
Module (alertes chargées par l'appli) : `bosses/gigalodon.yaml`. Relevé complet : `bosses/reference/gigalodon.yaml` (06/11/2026).

## En une phrase
On tient 3 tours, et le score dépend des dégâts infligés. Le boss joue deux fois par tour et punit le regroupement, les côtés, les bords et la mêlée.

## Déroulement
| Moment | Ce qui se passe |
|---|---|
| Début de chaque tour | 1ʳᵉ action du boss + attrape le personnage en mêlée |
| Moitié des joueurs ont joué | 2ᵉ action du boss |
| Tour 3 | La map s'assombrit (dernier tour) |
| Début du tour 4 | Gigalodoom : victoire automatique |

## Sorts
| Sort | Dégâts | Zone | Parade |
|---|---|---|---|
| Gigarâle | 700 terre, 1×/tour | Persos à ≤ 2 PO d'un allié, se propage | 3 cases d'écart |
| Maxquale | 500 air, 5×/tour, 1×/cible | Portée infinie sans ligne de vue | À encaisser |
| Ultrasplash | 700 eau, 1×/tour | Cônes latéraux | Diagonale, résistances eau |
| Tournageoire | 700 terre, 1×/tour | Cercle T6, poussée de 7 | Loin des bords |

## Les dents de l'amer
3 cases de mêlée devant la gueule. Un personnage dessus est attrapé, passe son tour, et un glyphe noir apparaît.
- Un allié sur le glyphe au tour suivant : le captif est avalé et un nouveau personnage est attrapé.
- Glyphe libre : le captif est recraché (dégâts = 80 % de ses PV actuels), puis il ne peut plus être attrapé pendant 1 tour.

⚠️ Les sources divergent (Sigilos : un allié sur le glyphe = le captif meurt). **À vérifier en jeu.**

## Détection (capture d'écran uniquement)
- Compteur de tours : la machine au bord de la map (OCR). Une seule source le mentionne.
- Dernier tour : chute de luminosité de la zone de jeu.
- Glyphe noir et glyphe rouge (hitbox) : détection de couleur sur la grille.
- 2ᵉ action : pas d'indice visuel fiable connu → raccourci manuel en priorité.

## Stats (wiki)
Niveau 220, 1 000 000 000 PV, 15 PA, 0 PM, 0 % de résistances, ne peut pas être déplacé.

## À vérifier en jeu (fixtures à capturer)
1. Le compteur de tours : position et lisibilité OCR.
2. La règle exacte du glyphe noir.
3. Un repère visuel pour la 2ᵉ action.
4. Les équilibrages depuis la 3.7.

## Sources
- [Dofus pour les Noobs](https://www.dofuspourlesnoobs.com/gouffre-du-gigalodon.html) (29/06/2026)
- [Sigilos](https://beta.sigilos.fr/guides/raid-gigalodon-dofus-guide) (27/09/2026)
- [Wiki Dofus](https://dofuswiki.fandom.com/wiki/Gigalodon)
- [Zeminal](https://zeminal.tech/types-de-raid/2/guide)
