# CARTE du dépôt DBMDofus

Équivalent de Deadly Boss Mods pour Dofus 3 (guilde No Try No Gain). Overlay externe et passif.
Partie rédigée (§1-§6) à tenir à jour à la main ; §7 est généré par `python outils/carte_index.py`.

## 1. Architecture
```
dbmdofus/
  __main__.py     point d'entrée (python -m dbmdofus [--boss ID] [--apercu f.png])
  app.py          assemblage : boucle QTimer, actions des raccourcis
  config.py       réglages (fps, seuil de confiance, zones, raccourcis, position overlay)
  theme.py        SEUL fichier de couleurs (DA « nuit aux lucioles »)
  boss_loader.py  bosses/*.yaml -> Boss / Phase / Mecanique (validation)
  combat_state.py machine à états du combat (tour, phase, priorité manuelle)
  alerts.py       alertes du tour courant + préavis
  capture.py      capture mss limitée aux zones (chemin chaud)
  ocr.py          Lecture(valeur, confiance), moteur OCR enfichable, détection de motif
  hotkeys.py      raccourcis globaux (pynput) -> signal Qt
  overlay.py      fenêtre transparente, au premier plan, clics traversants
bosses/<boss>.yaml    module d'un boss (format du chargeur : phases, mécaniques par tour, alertes)
docs/bosses/<boss>.md doc lisible du boss
bosses/reference/<id>.yaml      relevé des mécaniques (131 boss : raids + donjons), NON chargé par l'appli
docs/bosses/reference/<id>.md   doc générée depuis la fiche de référence
outils/valider_reference.py     validation des fiches de référence (+ couverture de l'index des donjons)
outils/generer_docs_reference.py génère docs/bosses/reference/*.md (n'écrase pas une doc manuelle)
outils/sources/index_donjons.tsv index des 122 donjons (boss, niveau, position, URL du guide)
outils/carte_index.py génère §7
tests/                pytest (+ tests/fixtures/ : captures PNG pour l'OCR)
```

## 2. Flux de données
`QTimer (app.boucle)` → `Capture.saisir("tour")` → `MoteurOCR.lire()` → `Lecture(valeur, confiance)`
→ `EtatCombat.lecture_tour()` → `alerts.alertes_courantes()` → `Overlay.rafraichir()`.
Saisie manuelle : `Raccourcis.action` (signal) → `Application.executer()` → `EtatCombat.tour_manuel()/…` → overlay.

Règle de priorité : une lecture OCR n'est appliquée que si confiance ≥ `seuil_confiance` (0,80),
jamais à reculons, et, après une saisie manuelle, seulement si elle annonce le tour suivant.

## 3. Dépendances (chacune justifiée)
| Paquet | Pourquoi |
|---|---|
| PySide6 | overlay transparent, clics traversants, boucle d'évènements, signaux inter-threads |
| mss | capture d'écran rapide par zone, sans dépendance système |
| numpy | images en tableaux (format natif de mss et OpenCV) |
| opencv-python-headless | prétraitement OCR, détection de motifs (matchTemplate) ; version headless = plus légère |
| PyYAML | lecture des fichiers de boss |
| pynput | raccourcis globaux (écoute seulement, aucune frappe envoyée) |
| pytest (dev) | tests |

Moteur OCR : **pas encore choisi** (voir REPRISE.md). Candidat : RapidOCR (pip seul, sans binaire externe).

## 4. Conventions
- **CGU Ankama** : capture d'écran + OCR/détection d'images et raccourcis seulement. Pas de lecture mémoire,
  pas de paquets, pas d'injection, pas d'action en jeu. `tests/test_regles.py` refuse les API interdites.
- **Données ≠ code** : aucune mécanique en dur. Un boss = `bosses/<id>.yaml` + `docs/bosses/<id>.md`
  (champ `doc` obligatoire, vérifié par test).
- **Couleurs** : uniquement dans `theme.py` (vérifié par test). Or = mise en valeur, vert = agir.
- **Textes** de l'interface en français.

## 5. Garde-fous de performance
- Cible < 5 % CPU. Boucle à 2 img/s par défaut (`Config.fps`).
- Jamais l'écran entier : seulement `Config.zones`.
- `mss` instancié une fois ; conversion BGRA→BGR sans copie.
- `Capture.ms_derniere` / `ms_moyenne` : mesure ms par image, à relever avant/après toute modification du chemin chaud.
- Sans moteur OCR disponible, la boucle ne démarre pas du tout.
- Overlay redessiné seulement quand l'état change.

## 6. Recettes
**Ajouter un boss** : copier `bosses/exemple.yaml` en `bosses/<id>.yaml`, renseigner `id`, `nom`, `doc`,
phases (`debut: {tour: N}` ou rien pour une phase manuelle), mécaniques (`tours: [..]` ou `tous_les` +
`a_partir_de`, `phase` facultative, `alerte: {texte, niveau, avance}`) ; écrire `docs/bosses/<id>.md` ;
`pytest` ; `graphify update . && graphify cluster-only .` ; `python outils/carte_index.py`.
Niveaux : `info`, `important`, `critique`, `action`.

**Passer un boss de la référence au module** : partir de `bosses/reference/<id>.yaml` (sorts, mécaniques,
`alertes` en texte libre), écrire `bosses/<id>.yaml` au format du chargeur ; garder les textes d'alerte
courts (≈ 35 caractères : l'overlay ne gère pas encore les retours à la ligne). Exemple : `gigalodon`.

**Fiches de référence** : obligatoires `id`, `nom`, `type` (`donjon`|`raid_guilde`), `contenu`,
`fiabilite` (`confirme`|`source_unique`|`a_verifier`), `sources` ; `python outils/valider_reference.py`
puis `python outils/generer_docs_reference.py`. Mise en garde : les donjons viennent surtout de guides
JeuxOnLine écrits avant Dofus 3, à vérifier en jeu.

**Raccourcis par défaut** : Ctrl+Alt+D début · F fin · N tour suivant · B tour précédent · P phase suivante · M boss suivant.

**Aperçu de l'overlay** : `python -m dbmdofus --apercu apercu.png` (combat simulé au tour 3).

## 7. Index (généré)
<!-- INDEX:DEBUT -->
### Modules
- `dbmdofus/__init__.py` — DBMDofus : alertes de mécaniques de boss pour Dofus 3 (overlay passif).
- `dbmdofus/__main__.py` — Point d'entrée : python -m dbmdofus [--boss ID] [--apercu fichier.png]
  - `main()` (l.13)
- `dbmdofus/alerts.py` — Calcul des alertes à afficher pour le tour et la phase courants.
  - classe `Alerte` (l.10) : libelle
  - `alertes_courantes()` (l.22)
- `dbmdofus/app.py` — Assemblage : config, boss, état, raccourcis, boucle de capture, overlay.
  - classe `Application` (l.20) : demarrer, boucle, executer, boss_suivant, rafraichir, arreter
- `dbmdofus/boss_loader.py` — Chargeur de modules de boss : bosses/<boss>.yaml -> objets Boss validés.
  - classe `BossInvalide` (l.18)
  - classe `Phase` (l.23)
  - classe `Mecanique` (l.30) : tombe_au_tour
  - classe `Boss` (l.50) : phase
  - `_exiger()` (l.63)
  - `boss_depuis_dict()` (l.69)
  - `charger_boss()` (l.108)
  - `charger_tous()` (l.113)
- `dbmdofus/capture.py` — Capture d'écran limitée aux zones utiles (mss). Chemin chaud.
  - classe `Capture` (l.13) : _mss, saisir, fermer
- `dbmdofus/combat_state.py` — Machine à états du combat : en combat ou non, tour, phase.
  - classe `Source` (l.16)
  - classe `EtatCombat` (l.22) : debut_combat, fin_combat, changer_boss, tour_manuel, tour_suivant, tour_precedent, phase_manuelle, phase_suivante, lecture_tour, _maj_phase_auto, _noter
- `dbmdofus/config.py` — Réglages par défaut : zones d'écran, fréquence de capture, raccourcis.
  - classe `Config` (l.16)
- `dbmdofus/hotkeys.py` — Raccourcis globaux (saisie manuelle). Écoute le clavier, n'envoie rien au jeu.
  - classe `Raccourcis` (l.15) : demarrer, arreter
- `dbmdofus/ocr.py` — Lecture d'images : OCR et détection de motifs, toujours avec confiance.
  - classe `Lecture` (l.18) : nombre
  - classe `MoteurOCR` (l.27) : lire
  - classe `MoteurAucun` (l.33) : lire
  - `preparer()` (l.41)
  - `detecter_motif()` (l.50)
- `dbmdofus/overlay.py` — Overlay transparent, toujours au premier plan, que les clics traversent.
  - classe `Overlay` (l.13) : _label, rafraichir, paintEvent
- `dbmdofus/theme.py` — Thème « nuit aux lucioles » : SEUL fichier où des couleurs sont écrites.
  - `couleur_niveau()` (l.28)
- `outils/carte_index.py` — Régénère l'index automatique de CARTE.md (entre les balises INDEX).
  - `_resume()` (l.21)
  - `index_module()` (l.26)
  - `index_bosses()` (l.41)
  - `generer()` (l.51)
  - `main()` (l.61)
- `outils/generer_docs_reference.py` — Génère docs/bosses/reference/<id>.md à partir de bosses/reference/<id>.yaml.
  - `_liste()` (l.15)
  - `rendre()` (l.21)
  - `main()` (l.45)
- `outils/valider_reference.py` — Vérifie les fiches de référence bosses/reference/*.yaml (relevé des mécaniques, pas des modules
  - `main()` (l.23)
- `tests/conftest.py`
  - `qapp()` (l.9)
- `tests/test_bosses.py`
  - `test_tous_les_boss_sont_valides_et_documentes()` (l.9)
  - `test_recurrence()` (l.19)
  - `test_boss_invalides()` (l.32)
  - `test_fichier_invalide_ignore()` (l.37)
- `tests/test_combat.py`
  - `etat()` (l.10)
  - `test_ocr_faible_confiance_ignoree()` (l.14)
  - `test_ocr_accepte_et_phase_auto()` (l.20)
  - `test_ocr_ne_recule_pas()` (l.26)
  - `test_manuel_prend_le_dessus()` (l.32)
  - `test_phase_manuelle_bloque_phase_auto()` (l.42)
  - `test_alertes_et_preavis()` (l.49)
  - `test_pas_alerte_hors_combat()` (l.57)
- `tests/test_ocr.py`
  - `_image_avec_texte()` (l.12)
  - `test_lecture_nombre()` (l.18)
  - `test_moteur_aucun()` (l.23)
  - `test_preparer_binarise()` (l.28)
  - `test_detecter_motif()` (l.33)
  - `test_fixtures_lisibles()` (l.41)
- `tests/test_overlay.py`
  - `test_overlay_rendu()` (l.8)
- `tests/test_reference.py` — Fiches de référence (bosses/reference/) : valides, documentées, invisibles pour le chargeur.
  - `test_fiches_reference_valides()` (l.11)
  - `test_chaque_fiche_a_sa_doc()` (l.19)
  - `test_reference_non_chargee_comme_module()` (l.25)
- `tests/test_regles.py` — Règles du projet vérifiées automatiquement.
  - `test_aucune_couleur_en_dur_hors_theme()` (l.10)
  - `test_cgu_pas_de_memoire_paquets_ni_actions()` (l.16)

### Boss
- `bosses/exemple.yaml` — Gardien d'exemple : 3 phase(s), 3 mécanique(s), doc `docs/bosses/exemple.md`
- `bosses/gigalodon.yaml` — Gigalodon : 1 phase(s), 6 mécanique(s), doc `docs/bosses/gigalodon.md`
<!-- INDEX:FIN -->
