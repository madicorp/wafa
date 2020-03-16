# WAFA Fertilizer
A wagtail App

## Requirements

Python >= 2.7

## Install work environment

if virtualenv is not installed <br>

`pip install virtualenv`

Create virtualenv <br>

`virtualenv venv`

Install dependencies <br>

`pip install -r requirements.txt`

## Activate venv

`source venv/bin/activate`

## Launch locally

`./manage.py migrate` <br>
`./manage.py createsuperuser` <br>

**lauch server** <br>
`./manage.py runserver` <br>

Deployed on `http://127.0.0.1:8000/` <br>
Admin page accessible at `http://127.0.0.1:8000/admin/`

## Update model

`./manage.py makemigrations` <br>
`./manage.py migrate`

## Update i18n
`./manage.py compilemessages`

## Deploy on prod

- create a `config.yml` file base on `sample.config.yml` and set variables <br>
- change `os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wafa.settings.dev")` by `os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wafa.settings.production")` in `manage.py`

