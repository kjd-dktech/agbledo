# AgbleDɔ̀ : Détection Automatique de Maladies Végétales Tropicales

Ce projet vise à construire un système de détection automatique de maladies sur des cultures agricoles tropicales prioritaires au Togo (maïs et manioc) en utilisant la vision par ordinateur et l'apprentissage profond (YOLOv11). Ce système est conçu pour automatiser le diagnostic visuel, actuellement manuel et chronophage, réduisant le temps de détection par image.

## Contexte et Motivation
Le projet se concentre sur deux problèmes agricoles fondamentaux documentés au Togo :
- **La mosaïque du manioc** : Transmise par des virus (ACMV, EACMV, ICMV) causant des pertes allant jusqu'à 70%.
- **La chenille légionnaire d'automne (Spodoptera frugiperda)** : Une infestation sur le maïs occasionnant des dégâts majeurs, détectée localement dès 2016.

L'objectif de cette solution est de permettre une surveillance scalable sur téléphones mobiles, s'appuyant sur des travaux de recherche locaux (ESA/Université de Lomé).

## Sources de Données
Pour des raisons de volumétrie, le répertoire `data/raw/` n'est pas versionné. Néanmoins, l'intégralité de la méthodologie de préparation et de traitement des données est publique et reproductible (voir `notebooks/` et `src/data/`). Les données s'appuient sur :
- **PlantVillage** : Référence scientifique en conditions contrôlées.
- **CCMT (Cassava & Maize)** : Données acquises en conditions réelles, incluant les maladies documentées localement.

## Bibliographie
Ce projet justifie ses classes et hypothèses par la littérature ouest-africaine :
- **Adjata K.D. et al. (2008)**. *Incidence of Cassava Viral Diseases ... in Togo*. American Journal of Plant Physiology.
- **Koffi D., Agboka K. et al. (2020)**. *Maize Infestation of Fall Armyworm within Agro-Ecological Zones of Togo and Ghana*. Environmental Entomology.

## Structure du Projet

- `data/` : Répertoire des données (brutes et traitées).
- `notebooks/` : Notebooks Jupyter.
- `src/` : Scripts de traitement des données, configuration du modèle et modules spécialisés.
- `configs/` : Fichiers YAML gérant les hyperparamètres et métadonnées du dataset.
- `models/` : Poids entraînés du modèle final (Hébergés ultérieurement).
- `runs/` : Expériences YOLO
- `mlruns` : Expériences MLFlow
- `tests/` : Tests

## Pipeline Technique

- **Modèle de Vision** : YOLOv11s (Ultralytics) — performant et optimisé.
- **Tracking Expérimental** : Expériences versionnées et suivies via [MLFLow](#).
- **Explicabilité** : Localisation des zones de prédiction via Grad CAM pour la confiance utilisateurs.
- **Déploiement** : 
  - API : Asynchrone sous FastAPI, packagée via Docker.
  - IHM : Interface finale servie par Streamlit pour un accès multi-support rapide.

## Réalisations

### Plan de réalisation 

#### Développement du modèle
- [x] Traitement des données
- [x] Architecture ML
- [x] Entraînement du classifieur
- [x] Évaluation formelle du classifieur
- [] Explicabilité du classifieur
- [] Benchmarks

#### Industrialisation
- [ ] Export ONNX
- [ ] Développement de l'API
- [ ] Interface IHM
- [ ] Conteneurisation (Docker)

#### Mise en production
- [ ] Déploiement
- [ ] Monitoring
- [ ] Maintenance

#### Documentation
- [ ] Documentation technique
- [ ] Guide utilisateur
- [ ] Documentation API

### Résultats actuels

- Modèle `agbledɔ01.pt` disponible sur [Hugging Face](https://huggingface.co/kjd-dktech/agbledo01)

---

