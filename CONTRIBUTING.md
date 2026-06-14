# Guide de Contribution

Merci de votre intérêt pour **AgbleDɔ̀** !

Ce projet vise à développer une solution open source de détection automatique des maladies végétales tropicales à l'aide de l'intelligence artificielle. Toute contribution est la bienvenue : amélioration du code, correction de bugs, documentation, tests, optimisation des modèles ou nouvelles fonctionnalités.

## Comment contribuer

### 1. Signaler un problème

Si vous identifiez un bug, une incohérence ou une amélioration possible :

1. Vérifiez qu'un ticket similaire n'existe pas déjà dans les Issues.
2. Ouvrez une nouvelle Issue en décrivant :

   * le problème observé ;
   * les étapes permettant de le reproduire ;
   * le comportement attendu ;
   * votre environnement de travail (OS, Python, versions des dépendances).

## 2. Proposer une amélioration

Les propositions suivantes sont particulièrement encouragées :

* amélioration des performances du modèle ;
* ajout de nouvelles cultures ou maladies ;
* optimisation du pipeline de traitement des données ;
* amélioration de l'explicabilité (Grad-CAM, visualisations, interprétabilité) ;
* développement de l'API FastAPI ;
* développement de l'interface Streamlit ;
* amélioration de la documentation ;
* ajout de tests automatisés.

## 3. Workflow Git

1. Forkez le dépôt.
2. Créez une branche dédiée :

```bash
git checkout -b feature/nom-de-la-fonctionnalite
```

ou

```bash
git checkout -b fix/description-du-correctif
```

3. Effectuez vos modifications.
4. Ajoutez ou mettez à jour les tests si nécessaire.
5. Vérifiez que les tests passent.
6. Commitez vos changements :

```bash
git commit -m "feat: ajout de ..."
```

7. Poussez votre branche :

```bash
git push origin feature/nom-de-la-fonctionnalite
```

8. Ouvrez une Pull Request.

## Standards de développement

### Configuration de l'environnement (Python 3.14)

Nous utilisons **Python 3.14**. Pour contribuer efficacement :
1. Créez votre environnement virtuel (`python3.14 -m venv venv` puis `source venv/bin/activate`).
2. Installez les dépendances (`pip install -r requirements.txt`).
3. Installez les outils de qualité de code (`pip install pytest ruff`).

### Qualité du code (Linting et Tests)

Afin d'assurer une base de code propre et maintenable, nous utilisons **Ruff** (un linter/formateur ultra-rapide) et **Pytest**.

Avant de soumettre une Pull Request, exécutez systématiquement :

```bash
# Pour formater le code automatiquement
ruff format src/ tests/

# Pour vérifier les standards (linting)
ruff check src/ tests/

# Pour exécuter les tests automatisés
pytest tests/
```

Les contributions qui ajoutent de nouvelles fonctionnalités doivent inclure des tests associés dans le dossier `tests/`.

### Format des Pull Requests

Lors de l'ouverture d'une Pull Request, merci d'inclure :
- Un lien vers l'Issue correspondante (si applicable).
- Une description claire du problème résolu ou de la fonctionnalité ajoutée.
- La confirmation que `ruff check` et `pytest` passent sans erreur localement.

## Structure du projet

```text
api/            API FastAPI
app/            Interface utilisateur
configs/        Fichiers de configuration
data/           Jeux de données
models/         Modèles entraînés
notebooks/      Expérimentations et analyses
src/            Scripts et Code source
tests/          Tests automatisés
```

## Données et modèles

Les contributeurs doivent respecter les licences associées aux jeux de données utilisés.

Les poids du modèle principal sont distribués séparément lorsque nécessaire.

Toute contribution impliquant un nouveau jeu de données doit documenter :

* la source ;
* la licence ;
* la méthode de collecte ;
* les éventuels prétraitements réalisés.

## Licence

En contribuant à ce projet, vous acceptez que votre contribution soit distribuée sous la même licence que le projet.

## Code de conduite

Les échanges doivent rester respectueux, constructifs et bienveillants.

Les comportements discriminatoires, insultants ou harcelants ne sont pas tolérés.

## Remerciements

Merci à toutes les personnes qui contribuent à rendre les technologies d'IA plus accessibles au service de l'agriculture africaine.
