WORKDIR = form_templates
MANAGE = python $(WORKDIR)/manage.py
BASE_MANAGE = python manage.py

default:
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	$(MANAGE) runserver

style:
	isort $(WORKDIR)
	black -S -l 79 $(WORKDIR)
	flake8 $(WORKDIR)
	mypy $(WORKDIR)

migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

run:
	$(MANAGE) runserver

test:
	$(MANAGE) test $(WORKDIR)

app: 
	cd $(WORKDIR); \
	$(BASE_MANAGE) startapp $(name); \
	cd ..

project:
	django-admin startproject $(name)

pip:
	python -m pip install --upgrade pip

req_file:
	pip freeze -> $(WORKDIR)/requirements.txt

req:
	pip install -r $(WORKDIR)/requirements.txt

style-req:
	pip install -r style-requirements.txt

fill:
	$(MANAGE) fill_database
