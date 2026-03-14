# Site web de l'UNF Montréal

Site web de l'[Unité de Neuroimagerie Fonctionnelle (UNF)](https://unfmontreal.github.io/fr), une plateforme de recherche en neuroimagerie affiliée au [CRIUGM](https://criugm.qc.ca). Ce site est construit avec [MyST Markdown](https://mystmd.org/) et [Jupyter Book v2](https://jupyterbook.org/).

[![Deploy](https://github.com/UNFmontreal/fr/actions/workflows/deploy.yml/badge.svg)](https://github.com/UNFmontreal/fr/actions/workflows/deploy.yml)

## Développement local

1. Cloner le dépôt
2. Installer les dépendances :
   ```bash
   pip install jupyter-book
   ```
3. Lancer le serveur de développement :
   ```bash
   myst start
   ```
   Ou générer le site statique :
   ```bash
   myst build --html
   ```
   Le résultat se trouve dans `_build/html/`.

## Déploiement

Tout push sur `main` déclenche un déploiement automatique sur GitHub Pages à l'adresse :
**https://unfmontreal.github.io/fr**

> Les paramètres GitHub Pages du dépôt doivent être configurés sur **GitHub Actions** (et non sur une branche).

## Contributions

Les contributions sont les bienvenues. Consultez la liste des contributeurs dans l'[onglet Contributors](https://github.com/UNFmontreal/fr/graphs/contributors).
