# Calendrier Liturgique et Agricole 2025

Générateur automatique de calendrier A3 paysage professionnel combinant informations liturgiques, agricoles et phases lunaires.

## Caractéristiques

- **Format** : A3 paysage (420mm x 297mm).
- **Structure** : 2 pages (6 mois par page).
- **Design** : 
    - Arrière-plan HD net (Église) sans flou ni masque sombre.
    - Interface flottante transparente pour une visibilité maximale de l'image.
    - Hiérarchie visuelle claire avec typographie contrastée.
    - En-tête institutionnel avec logos (Église, Agriculture, Rose de Luther) et photos.
- **Données Affichées** :
    - **Liturgie** : Couleurs liturgiques (bordure gauche), noms des dimanches, 4 lectures bibliques complètes.
    - **Agriculture** : Icônes de cultures (riz, manioc, haricot, maïs) et d'actions (semis, entretien, récolte).
    - **Astronomie** : Phases lunaires précises pour 2025.
    - **Événements** : Programme de l'église et jours fériés.

## Architecture du Projet

```text
├── main.py              # Script principal de génération PDF
├── config/              # Configuration des couleurs, polices et pages
├── data/                # Données CSV (Globales et Mensuelles)
│   ├── global/          # Paramètres globaux (en-têtes, couleurs, icons)
│   └── mois/            # Données spécifiques par mois (01-12)
├── layout/              # Logique de rendu des composants (lignes, en-têtes)
├── utils/               # Utilitaires (chargement CSV, calculs de dates, icons)
├── assets/              # Ressources (Images, Logos, Icons)
└── output/              # Dossier de sortie du PDF généré
```

## Installation et Utilisation

### Prérequis
- Python 3.10+
- Dépendances : `pandas`, `reportlab`, `pillow`

### Génération du Calendrier
Pour générer le fichier PDF, exécutez simplement :
```bash
python main.py
```
Le résultat sera disponible dans `output/calendrier_A3.pdf`.

## Personnalisation
Les données peuvent être modifiées directement dans les fichiers CSV du dossier `data/`. Le générateur synchronise automatiquement les IDs de couleurs et d'icônes entre les fichiers globaux et mensuels.
