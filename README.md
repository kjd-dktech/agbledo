# AgbleDɔ̀ : Détection Automatique de Maladies Végétales Tropicales

Ce projet vise à construire un système de détection automatique de maladies sur des cultures agricoles tropicales prioritaires au Togo (maïs et manioc) en utilisant la vision par ordinateur et l'apprentissage profond (YOLOv11). Ce système est conçu pour automatiser le diagnostic visuel, actuellement manuel et chronophage, réduisant le temps de détection par image.

## Contexte et Motivation
Le projet se concentre sur deux problèmes agricoles fondamentaux documentés au Togo :
- **La mosaïque du manioc** : Transmise par des virus (ACMV, EACMV, ICMV) causant des pertes allant jusqu'à 70%.
- **La chenille légionnaire d'automne (Spodoptera frugiperda)** : Une infestation sur le maïs occasionnant des dégâts majeurs, détectée localement dès 2016.

L'objectif de cette solution est de permettre une surveillance scalable sur téléphones mobiles, s'appuyant sur des travaux de recherche locaux (ESA/Université de Lomé).

## Structure du Projet

- `data/` : Répertoire des données (brutes et traitées).
- `notebooks/` : Notebooks Jupyter.
- `src/` : Scripts de traitement des données, configuration du modèle et modules spécialisés.
- `api/` : Code de l'API de prédiction.
- `app/` : Interface utilisateur web.
- `configs/` : Fichiers YAML gérant les hyperparamètres et métadonnées du dataset.
- `models/` : Poids entraînés du modèle final (Hébergés ultérieurement).

## Pipeline Technique

- **Modèle de Vision** : YOLOv11s (Ultralytics) — performant et optimisé.
- **Tracking Expérimental** : Expériences versionnées et suivies via [Weights & Biases (W&B)](#).
- **Explicabilité** : Localisation des zones de prédiction via pytorch-grad-cam pour la confiance utilisateurs.
- **Déploiement** : 
  - API : Asynchrone sous FastAPI, packagée via Docker.
  - IHM : Interface finale servie par Streamlit pour un accès multi-support rapide.

## Guide de Démarrage

### Pré-requis
- Docker et Docker Compose
- Python 3.1x+ pour exécution classique 

### Installation classique
Cloner le répertoire et instancier votre environnement virtuel :
```bash
git clone <url-du-repo>
cd AgbleDo_01
python -m venv agbledɔ01venv #ou source agbledɔ01venv/bin/activate
pip install -r requirements.txt
```

---

