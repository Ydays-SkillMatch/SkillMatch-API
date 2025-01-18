# SkillMatch

## Description

SkillMatch est une plateforme innovante dédiée aux entreprises et écoles de développement souhaitant évaluer les
compétences techniques de manière sécurisée. Ce système complet comprend un navigateur Linux personnalisé, un IDE en
ligne, et un serveur, garantissant un environnement 100 % contrôlé pour les évaluations techniques. Il limite les
risques de fraude grâce à des restrictions strictes, comme l'impossibilité d'installer des logiciels tiers ou des
extensions.

SkillMatch est conçu pour offrir une solution simple, rapide et sécurisée, déployable en moins d’une minute via une clé
USB, tout en permettant aux utilisateurs de créer des exercices, gérer des utilisateurs, et effectuer des évaluations
dans un environnement sécurisé. Cette plateforme est idéale pour les entreprises cherchant à tester les compétences de
leurs employés et les écoles offrant des évaluations pratiques en toute sécurité.

## Local Environement setup

### UV

Official documentation: [https://docs.astral.sh/uv/#highlights](https://docs.astral.sh/uv/#highlights)

Install UV using the following command:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Setup python

```bash
uv python install 3.13
```

### Direnv

Create a new venv at the root of the project: `uv venv`

Create envrc file with the following content to activate the virtual environment and set the environment variables

```
echo '. .venv/bin/activate
export DATABASE_URL="postgresql://localhost:5432/skillmatch?user=skillmatch&password=skillmatchpassword"
export DJANGO_SETTINGS_MODULE=skillmatch.settings.local' > .envrc
```

Instruct direnv to activate the venv when entering the project

[Refer to the documentation](https://direnv.net/docs/installation.html) for more information

When direnv is installed, run `direnv allow` to allow the .envrc file to be executed

### Setup the project

Install dependencies

```

uv sync

```

Then start the service containers (Postgres), migrate

```

docker-compose up -d
python manage.py migrate

```

Finally, start the server:

```

python manage.py runserver

```

## Access to the documentation

The documentation is available at the following URL: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)


