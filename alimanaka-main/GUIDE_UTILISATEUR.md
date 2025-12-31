# Guide Utilisateur - Calendrier FLM 2026

## 📅 Qu'est-ce que ce Calendrier ?

Ce calendrier combine :
- **Informations religieuses** : Dimanches, couleurs liturgiques, lectures bibliques
- **Informations agricoles** : Phases lunaires, cultures, actions agricoles optimales
- **Photos contextuelles** : 6 illustrations pour illustrer chaque calendrier

## 🚀 Démarrage Rapide (3 étapes)

### 1. Installation
```bash
pip install reportlab pandas pillow
```

### 2. Générer les PDFs
```bash
cd alimanaka-main
python main.py
```

### 3. Récupérer les fichiers
Les PDFs sont dans le dossier `output/` :
- `calendrier_A3.pdf` ← Impression grand format
- `calendrier_A4.pdf` ← Impression standard

## 📝 Modifier les Informations

### Changer le Nom de l'Église

Éditez `data/global/entetes.csv` :
```csv
ligne,id,texte
1,1,Ma Nouvelle Église Luthérienne
2,2,Synoda-Paritany ...
3,3,Fileovana ...
4,4,...
```

### Changer l'Année

Éditez `data/global/configuration.csv` et changez la valeur `annee` :
```csv
cle,valeur,description
annee,2027,Année du calendrier
...
```

### Changer le Nom du Designer

Éditez `data/global/configuration.csv` :
```csv
designer_info,Design & Mise en page : Votre Nom | Contact : 034 XX XX XX XX
```

### Ajouter/Modifier les Photos

Éditez `data/global/photos.csv` et mettez à jour les chemins :
```csv
numero_page,numero_photo,chemin,description
1,1,assets/images/photo_nouvelle.jpg,Photo de couverture
1,2,assets/images/photo2.jpg,Photo 2
```

## 📊 Modifier les Données Mensuelles

### Ajouter un Dimanche Spécial

Éditez `data/mois/[MOIS]/dimanches.csv` :
```csv
date,nom_dimanche,couleur_id,lecture1,psaume,lecture2,evangile
2026-01-04,Nom du Dimanche,vert,Lecture 1,Psaume,Lecture 2,Évangile
```

### Ajouter une Action Agricole

Éditez `data/mois/[MOIS]/programme_agricole.csv` :
```csv
date,culture_id,action_id
2026-01-15,riz,plantation
```

## 🎨 Personnaliser les Couleurs

Éditez `config/colors.py` pour modifier :
- Couleurs primaires (bleu foncé)
- Couleurs du texte
- Couleurs de fond

## 🔧 Dépannage

### Les PDFs ne se génèrent pas
- Vérifiez que Python 3.11+ est installé : `python --version`
- Vérifiez que les dépendances sont installées : `pip install reportlab pandas pillow`
- Vérifiez que le dossier `assets/images/` contient les photos

### Les données CSV ne s'affichent pas
- Vérifiez le codage du fichier : **UTF-8** (pas ANSI)
- Vérifiez les noms de colonnes (sensibles à la casse)
- Vérifiez que les fichiers CSV sont bien au bon endroit

### Les photos ne s'affichent pas
- Vérifiez que les chemins dans `photos.csv` sont corrects
- Vérifiez que les fichiers image existent
- Utilisez des chemins relatifs : `assets/images/photo1.jpg`

## 📞 Support Technique

- **Erreur de syntaxe Python** : Vérifiez la version de Python
- **Erreur de fichier manquant** : Vérifiez les chemins dans `configuration.csv`
- **Données qui n'apparaissent pas** : Vérifiez l'encodage UTF-8 des CSV

## 📋 Checklist Avant Impression

- [ ] Année correcte dans `configuration.csv`
- [ ] Nom de l'église à jour dans `entetes.csv`
- [ ] Photos présentes dans `assets/images/`
- [ ] Dimanches saisis pour tous les mois
- [ ] Couleurs liturgiques définies pour les dimanches
- [ ] Actions agricoles saisies pour la saison

## 📖 Structure d'un Jour

Chaque jour affiche :
```
[Numéro]  [Nom du jour]  [Couleur liturgique si dimanche]
[Informations du dimanche]
[Lectures bibliques]
[Programme d'église]
[Actions agricoles] [Phases lunaires]
```

## 🌙 Phases Lunaires Disponibles

- Nouvelle lune
- Premier quartier
- Pleine lune
- Dernier quartier

## 🌾 Cultures Disponibles

- Riz
- Manioc
- Maïs
- Haricot

## 🌱 Actions Agricoles Disponibles

- Plantation
- Récolte
- Entretien
- Semis

## ⛪ Couleurs Liturgiques

- **Vert** : Temps ordinaire
- **Blanc** : Fêtes du Christ
- **Rouge** : Martyrs / Esprit Saint
- **Violet** : Avent / Carême

---

**Besoin d'aide ?** Consultez le `README.md` pour les détails techniques.
