---
title: "Téléchargez vos données IRM"
date: 2020-10-18
description: >
  Récupération de vos données IRM
---

## Requis

Pour télécharger vos données il vous faut __[un compte](https://unf-montreal.ca/fr/documentation/welcome/account/)__ sur les serveurs de l'UNF.
Vous devez aussi connaitre le groupe auquel vous appartenez.

Vous avez deux façons différentes pour récupérer vos données IRM:
- Utiliser un terminal (Linux, Mac)
- Utiliser un client SFTP (Windows, Mac, Linux)

## Utilisation du terminal (Mac, Linux, Windows usagers avancés)

Ouvrez un terminal et utilisez la commande ssh pour récupérer vos données IRM dans une archive tar.gz. Remplassez les champs unf_login et le chemin vers vos dicoms ainsi que le fichier tar.gz de destination

- Télécharger un dossier et créer une archive tar.gz

`ssh unf_login@elm.criugm.qc.ca tar czf - /path/vers/vos/dicom/ > fichier_destination_sur_votre_ordinateur.tar.gz`

- Télécharger une archive tar.gz

`rsync -azvL unf_login@elm.criugm.qc.ca:/unf/dicoms/by_groups_tar/chemin_vers_vos_dicoms dossier_destination_sur_votre_ordinateur`

## Utilisation d'un client SFTP

### Installation

Filezilla est un logiciel que nous recommandons et qui est disponible sur tous les OS (Windows, Mac, Linux). Vous pouvez le télécharger en suivant le lien suivant __[Filezilla](https://filezilla-project.org/)__.

![Menu](/images/documentation/fr/download_mri/filezilla-menu.png)

### Configuration - première utilisation

Démarrez Filezilla et ouvrez le menu File -> Site Manager
Vous devriez obtenir la fenêtre suivante:

![Configuration](/images/documentation/fr/download_mri/filezilla-config.png)

Créez un nouveau site que vous pouvez nommer __unf-dicom__ par exemple et remplissez les différents champs:

**Host**: elm.criugm.qc.ca

**Protocol**: SFTP-SSH File Transfer Protocol

**Login Type**: Interactive

**User**: c'est le nom d'usager UNF qui vous a été créé lorsque vous avez fait __[votre demande de compte](https://unf-montreal.ca/fr/documentation/welcome/account/)__.

Ensuite cliquer sur le bouton *Connect*.

Vous pourriez voir apparaitre la fenêtre suivante:

![Certificate](/images/documentation/fr/download_mri/filezilla-trust.png)

Cliquez sur `Always trust` et cliquez sur OK.

Finalement Filezilla vous demandera votre mot de passe UNF comme présenté dans la fenêtre suivante:

![password](/images/documentation/fr/download_mri/filezilla-password.png)

Vous êtes maintenant connecté sur les serveurs de l'UNF et vous devriez avoir une fenêtre semblable.

![Main window](/images/documentation/fr/download_mri/filezilla-main_window.png)

- Rouge: votre système de fichier sur votre ordinateur.
- Bleu: le système de fichier sur le serveur.
- Vert: chemin utilisé sur le serveur

Vous pouvez déplacer des fichiers de droite à gauche ou inversement pour télécharger et/ou envoyer des données sur le serveur.


## Accès à vos données IRM

Vos données IRM peuvent se trouver à 3 différents endroits. Remplacer groupName par votre groupe.

- `/unf/bids/groupName` si vous avez demandé/coordonné une conversion BIDS automatique
- `/unf/dicoms/by_groups_tar/groupName` si vos données sont relativement vieilles (avant 2016)
- `/unf/dicoms/by_groups/groupName` si vos données ont été acquises plus récemment

Si vous souhaitez obtenir de l'aide pour télécharger vos données n'hésitez pas à envoyer un courriel à l'adresse suivante: __[support.unf](mailto:support.unf@criugm.qc.ca?subject=Help-Download-MRI)__.
