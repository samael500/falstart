ifndef CI_FLAG
	VENV_PATH := venv/bin/
else
	VENV_PATH :=
endif

install:
	ln -fs $(shell pwd)/falstart/falstart.py /usr/local/bin/falstart

pep8:
	$(VENV_PATH)pep8 --max-line-length=119 --show-source  falstart/

pyflakes:
	$(VENV_PATH)pylama -l pyflakes falstart/

lint:
	make pep8
	make pyflakes

test:
	# TODO: run test when it be

ci_test:
	make test
	make lint
