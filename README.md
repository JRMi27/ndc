# Pixel Heist — Nuit du Code

## Histoire

Tu incarnes un **braqueur en fuite**, qui vient de dérober les cramptés à la banque d'Apagnan City.
La police est à tes trousses — défends-toi contre les forces nationales et survive le plus longtemps possible !

---

## Lancer le jeu

**Prérequis :** Python 3 et la bibliothèque [Pyxel](https://github.com/kitao/pyxel)

```bash
pip install pyxel
python ndc.py
```

---

## Touches

### Déplacement
| Touche | Action |
|--------|--------|
| `Z` | Avancer (haut) |
| `Q` | Aller à gauche |
| `S` | Reculer (bas) |
| `D` | Aller à droite |

### Direction de tir
| Touche | Direction |
|--------|-----------|
| `↑` | Tirer vers le haut |
| `→` | Tirer vers la droite |
| `↓` | Tirer vers le bas |
| `←` | Tirer vers la gauche |

> Le personnage tire **automatiquement** toutes les 0,5 secondes dans la direction choisie.

### Autres
| Touche | Action |
|--------|--------|
| `ESPACE` | Easter egg |
| `G` | Recommencer (écran game over) |
| `F` | Quitter (écran game over) |

---

## Ennemis

Élimine tous les ennemis d'une vague pour passer à la suivante.

| Ennemi | Indicateur | Vitesse | PV | Points |
|--------|-----------|---------|-----|--------|
| Basique | Aucun | Lente | 1 | 10 pts |
| Rapide | Point jaune au-dessus | Rapide | 1 | 25 pts |
| Tank | Barre de vie rouge | Très lente | 3 | 75 pts |

---

## Vagues

| Vague | Basiques | Rapides | Tanks |
|-------|----------|---------|-------|
| 1 | 4 | — | — |
| 2 | 4 | 2 | — |
| 3 | 4 | 3 | 1 |
| 4 | 5 | 4 | 2 |
| 5 | 6 | 5 | 3 |
| 6+ | Augmente | Augmente | Augmente |

---

## Potions

Des potions apparaissent sur la carte. Marche dessus pour les ramasser.
Quand toutes les potions sont ramassées, de nouvelles apparaissent.
Si tu es blessé, tu as **40 % de chances** qu'une potion de soin apparaisse.

| Potion | Point coloré | Effet | Durée |
|--------|-------------|-------|-------|
| Vitesse | Jaune | +1,0 de vitesse | 8 secondes |
| Soin | Rose | +1 vie (max 3) | Instantané |
| Bouclier | Bleu | Invincibilité totale | 4 secondes |

> Quand le bouclier est actif, un **contour bleu** entoure le personnage.
> Le HUD affiche `SPD Xs` et `SCU Xs` (secondes restantes) en haut à droite.

---

## HUD (interface en jeu)

```
Vies:3        SPD 8s
Score:0       SCU 4s
Vague:1
```

| Élément | Description |
|---------|-------------|
| `Vies` | Nombre de vies restantes (max 3) |
| `Score` | Points accumulés |
| `Vague` | Numéro de la vague actuelle |
| `SPD Xs` | Boost de vitesse actif, X secondes restantes |
| `SCU Xs` | Bouclier actif, X secondes restantes |

---

## Mécanique de survie

- Quand un ennemi te touche, tu perds **1 vie** et tu retournes au centre de la carte
- Tous les ennemis sont **repoussés aux bords** pour te laisser le temps de réagir
- Tu es **invincible 1,5 seconde** après avoir été touché (le personnage clignote)
- À **0 vie** : game over — ton score et la vague atteinte sont affichés
