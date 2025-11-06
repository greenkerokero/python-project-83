# Page analyzer
[![Actions Status](https://github.com/greenkerokero/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/greenkerokero/python-project-83/actions)
[![Python CI](https://github.com/greenkerokero/python-project-83/actions/workflows/python-ci.yml/badge.svg)](https://github.com/greenkerokero/python-project-83/actions/workflows/python-ci.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=greenkerokero_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=greenkerokero_python-project-83)

A web application that analyzes specified websites for SEO suitability: it checks their accessibility and analyzes H1, title, and description tags.

## Demonstration
You can view application at the [provided link](https://python-project-83-0ff4.onrender.com/).

## Technologies used
- Python
- Flask + jinja
- HTML/CSS
- Bootstrap
- PostgreSQL

## Installation
For installation [UV package manager](https://docs.astral.sh/uv/getting-started/installation/) is required. After installing UV, clone the repository:
```
git clone https://github.com/greenkerokero/python-project-83.git
```
Go to the project folder:
```
cd python-project-83
```
Install dependencies using UV:
```
make install
```
In the root of the project, create a *.env* file with your key values and database access:
```
export SECRET_KEY=your_key_for_flask_app
export DATABASE_URL=postgresql://[db_user]:[db_password]@localhost:5432/[db_name]
```

## Usage
Start app using Gunicorn. Server is available at [0.0.0.0:8000](0.0.0.0:8000).
```
make start
```

Start in debug mode. Developmen servser is available at [127.0.0.1:5000](127.0.0.1:5000).
```
make dev
```
