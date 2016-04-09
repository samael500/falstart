VENV_PATH := venv/bin

install:
	ln -fs $(shell pwd)/falstart.py /usr/local/bin/falstart

pep8:
	$(VENV_PATH)/pep8 --exclude=*migrations*,*settings_local.py* --max-line-length=119 --show-source  {{ proj_name }}/

pyflakes:
	$(VENV_PATH)/pylama --skip=*migrations* -l pyflakes {{ proj_name }}/

lint:
	make pep8
	make pyflakes

# test:
# 	$(VENV_PATH)/python manage.py test -v 2 --noinput
