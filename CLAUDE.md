# UNF Montréal — French site (MyST/Jupyter Book v2)

## Project context

This is a rewrite of the UNF Montréal website using MyST markdown and Jupyter Book v2.

- **This repo (new):** https://github.com/UNFmontreal/fr
- **Old Hugo codebase:** https://github.com/UNFmontreal/unf-montreal.ca
- **MyST formatting inspiration:** https://github.com/SIMEXP/simexp.github.io

## Stack

- [Jupyter Book v2](https://jupyterbook.org) (powered by [mystmd](https://mystmd.org))
- Site config and TOC: `myst.yml`
- Deployed via GitHub Actions to GitHub Pages at `https://unfmontreal.github.io/fr`
- GitHub Pages source must be set to **GitHub Actions** (not a branch)

## Content migration

French content was migrated from `content/fr/` in the old Hugo repo. The migration script is `migrate.py` — re-run it if pulling updated content from the old repo.

Hugo-specific frontmatter fields (`type`, `draft`, `bg_image`, `weight`, etc.) are stripped. Only `title`, `date`, and `description` are kept.

## Structure

```
myst.yml                  # site config + full TOC
intro.md                  # landing page
about.md                  # about the UNF
team.md                   # team gallery (grid layout)
contact.md
rate.md
welcome/                  # onboarding docs
facility/                 # MRI facility, reservation, urgency procedures
your_study/               # study setup, MRI config, visit
your_data/                # data storage, download, preprocessing, analysis
course/                   # training: safety, compute canada, globus
documents/                # forms, logos, COVID docs
images/                   # logo and documentation images
.github/workflows/        # GitHub Actions deploy workflow
```

## Build locally

```bash
pip install jupyter-book
jupyter-book build --html
```

Output is in `_build/html/`.
