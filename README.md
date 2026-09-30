# Reading Copilot

Reading Copilot est un assistant de lecture basé sur l'intelligence artificielle, conçu pour aider les lecteurs à comprendre les mots, expressions et passages difficiles sans interrompre le rythme de leur lecture.

L'objectif est simple :
> Comprendre un texte sans quitter son application de lecture.


## Ce que fait Reading Copilot

- Sélectionner un mot ou un passage.
- Récupérer quelques mots autour du passage.
- Demander une explication à l'IA.
- Afficher l'explication dans une petite fenêtre.
- Écrire directement un texte, un mot ou même un paragraphe.
- Garder un historique des explications.
- Rechercher dans l'historique.
- Supprimer des éléments de l'historique.

## Technologies utilisées

- Python
- PySide6
- Google Gemini API
- SQLite
- Windows UI Automation
- pynput
- pyperclip

## Organisation du projet

Le projet est séparé en plusieurs parties:

- `ui/` : interface graphique
- `services/` : fonctionnalités de l'application
- `data/` : données locales
- `main.py` : lancement de l'application

## Installation

1 - Créer un environnement Python dans le terminal par le script:

```bash
python -m venv venv
```
2 - Active le par:

```bash
venv\Scripts\activate
```
3 - Installer les dépendances :

```bash
pip install -r requirements.txt
```
4 - Dans "api.env" mets ta clé api google pour utiliser gemini:

GEMINI_API_KEY=ta_cle_api

5 - Puis lancer:

```bash
python main.py
