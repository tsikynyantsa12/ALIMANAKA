# Alimanaka - Calendrier FLM 2026

## 🎯 État Final du Projet

**Statut:** ✅ COMPLÉTÉ ET PRÊT À L'EMPLOI

### Génération de Calendriers
- **Format A3 Paysage:** output/calendrier_A3.pdf (1.8 MB)
- **Format A4 Paysage:** output/calendrier_A4.pdf (1.8 MB)
- Tous les PDFs générés avec succès

## 📋 Structure Finale

```
alimanaka-main/
├── main.py                          # Script principal de génération
├── config/
│   ├── page.py                      # Configuration des pages
│   └── colors.py                    # Palette de couleurs
├── layout/
│   ├── day_row.py                   # Rendu des lignes de jours
│   └── day_details.py               # Détails des jours
├── utils/
│   ├── csv_loader.py                # Chargement CSV dynamique
│   ├── icon_mapper.py               # Mapping des icônes
│   └── date_utils.py                # Utilitaires de dates
├── data/
│   ├── global/
│   │   ├── mois.csv                 # Noms des mois (Malagasy)
│   │   ├── couleurs_liturgiques.csv # 4 couleurs (Vert, Rouge, Violet, Blanc)
│   │   ├── configuration.csv        # Année et paramètres
│   │   ├── phases.csv               # Phases lunaires
│   │   ├── cultures.csv             # Cultures agricoles
│   │   └── actions.csv              # Actions agricoles
│   └── mois/[01-12]/
│       └── Fichiers de données mensuelles
├── assets/                          # Icônes et images
├── output/                          # PDFs générés
├── README.md                        # Docs techniques (FR)
└── GUIDE_UTILISATEUR.md             # Guide utilisateur (FR)
```

## 🎨 Mise en Page Finale - Légende

**4 sections organisées:**
- **Haut-Gauche:** Phases lunaires (3 icônes)
- **Haut-Droit:** Cultures agricoles (3 icônes)
- **Bas-Gauche:** Actions agricoles (4 icônes sur 2 colonnes)
- **Bas-Droit:** Couleurs liturgiques (4 couleurs sur 2 colonnes)

**Amélioration récente:**
- Interligne amélioré (9pt)
- Tailles de police augmentées pour meilleure lisibilité
- Significations liturgiques compactes affichées
- Description supprimée (CSV nettoyé)

## 📊 Données Dynamiques

Toutes les données chargées depuis CSV :
- ✅ Noms des mois (Malagasy uniquement)
- ✅ Couleurs liturgiques (signification incluse)
- ✅ Phases lunaires, cultures, actions agricoles
- ✅ Configurations générales (année, etc.)

## 🚀 Utilisation

```bash
cd alimanaka-main
python main.py
# Génère : output/calendrier_A3.pdf + output/calendrier_A4.pdf
```

## ✅ Dernières Modifications

- Suppression colonne "description" du CSV couleurs_liturgiques
- Augmentation tailles de police dans légende
- Amélioration interligne (7pt → 9pt)
- Intégration significations liturgiques dans légende

**Date complétée:** 31 Décembre 2025
