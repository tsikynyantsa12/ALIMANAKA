# Calendrier Agricole et Liturgique FLM 2026

## Présentation du Projet

Ce projet génère un calendrier annuel complet combinant :
- **Informations liturgiques** : Couleurs liturgiques (Avent, Carême, Temps ordinaire, etc.)
- **Données agricoles** : Phases lunaires, cultures et actions agricoles  
- **Informations pastorales** : Dimanches, lectures bibliques et programme d'église
- **Illustrations** : Photos contextuelles (6 par calendrier)

Le calendrier est généré en deux formats : **A3** et **A4 paysage** avec marges de sécurité de 10mm.

## Structure des Dossiers

```
alimanaka-main/
├── assets/                          # Ressources (images, icônes)
│   ├── images/                      # Photos et logos
│   └── icons/                       # Icônes (phases lunaires, cultures, actions)
├── config/                          # Configuration du design
│   ├── colors.py                    # Palette de couleurs
│   ├── fonts.py                     # Styles et tailles de police
│   └── page.py                      # Dimensions et marges
├── data/                            # Données du calendrier
│   ├── global/                      # Données globales (CSV)
│   │   ├── couleurs_liturgiques.csv # Couleurs et significations
│   │   ├── cultures.csv             # Cultures agricoles
│   │   ├── actions_agricoles.csv    # Actions agricoles
│   │   ├── phases_lunaires.csv      # Phases de la lune
│   │   ├── entetes.csv              # En-tête (nom église, synodal, etc.)
│   │   ├── mois.csv                 # Noms des mois
│   │   ├── photos.csv               # Références aux photos
│   │   └── configuration.csv        # Année, designer, chemins logos
│   └── mois/                        # Données mensuelles (01-12)
│       └── [01-12]/
│           ├── dimanches.csv        # Liturgie des dimanches
│           ├── jours_feries.csv     # Jours fériés
│           ├── phases_lunaires.csv  # Phases lunaires mensuelles
│           ├── programme_agricole.csv
│           └── programme_eglise.csv
├── layout/                          # Fonctions de mise en page
│   ├── day_row.py                   # Affichage ligne-jour
│   └── month_block.py               # Bloc mensuel
├── utils/                           # Utilitaires
│   ├── csv_loader.py                # Chargement des données
│   ├── date_utils.py                # Utilitaires de date
│   └── icon_mapper.py               # Mappage des icônes
├── output/                          # PDFs générés
│   ├── calendrier_A3.pdf
│   └── calendrier_A4.pdf
├── main.py                          # Script principal
├── pyproject.toml                   # Configuration du projet
└── README.md
```

## Installation

### Prérequis
- Python 3.11+

### Installation des dépendances

```bash
# Avec pip
pip install reportlab pandas pillow

# Ou avec uv
uv add reportlab pandas pillow
```

## Guide Rapide : Modifier les Données

Tous les éléments du calendrier se modifient via les fichiers CSV :

| Fichier | Contenu | Localisation |
|---------|---------|--------------|
| `entetes.csv` | Nom église, synodal, lieu | `data/global/` |
| `mois.csv` | Noms des mois (malgache) | `data/global/` |
| `configuration.csv` | Année, designer, logos | `data/global/` |
| `photos.csv` | Chemins des 6 photos | `data/global/` |
| `couleurs_liturgiques.csv` | Couleurs + significations | `data/global/` |
| `dimanches.csv` | Liturgie par dimanche | `data/mois/[01-12]/` |
| `programme_agricole.csv` | Actions agricoles mensuelles | `data/mois/[01-12]/` |

## Générer le Calendrier

```bash
cd alimanaka-main
python main.py
```

Les PDFs sont générés dans `output/` :
- `calendrier_A3.pdf` (2 pages format A3)
- `calendrier_A4.pdf` (2 pages format A4)

## Personnalisation du Design

Modifiez les fichiers `config/` :
- **colors.py** : Couleurs primaires, texte, fond
- **fonts.py** : Polices et tailles
- **page.py** : Marges (actuellement 10mm de sécurité)

## Marges et Format

- **Format** : A4 Paysage (Landscape)
- **Marges de sécurité** : 10mm (28pt) sur les 4 côtés
- **Pages** : 2 pages (mois 1-6 et mois 7-12)

## Structure du Code Principal

### main.py
- `draw_header()` : En-tête avec logo, infos, année
- `draw_technical_legend()` : Légende unique (Lunes, Cultures, Actions, Couleurs)
- `draw_month()` : Bloc mensuel
- `draw_page()` : Assemblage complet d'une page
- `generate_calendar()` : Génération des PDFs

### utils/csv_loader.py
- `get_global_data()` : Charge toutes les données CSV globales
- `get_month_data()` : Charge les données d'un mois
- `get_config_value()` : Récupère une valeur de configuration

## Support

Pour plus de détails : voir `GUIDE_UTILISATEUR.md`
