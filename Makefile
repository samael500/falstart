VENV_PATH := venv/bin

install:
	ln -fs $(shell pwd)/falstart/falstart.py /usr/local/bin/falstart

pep8:
	$(VENV_PATH)/pep8 --max-line-length=119 --show-source  falstart/

pyflakes:
	$(VENV_PATH)/pylama -l pyflakes falstart/

lint:
	make pep8
	make pyflakes

# test:
# 	$(VENV_PATH)/python manage.py test -v 2 --noinput
