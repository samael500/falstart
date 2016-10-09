ifndef CI_FLAG
	VENV_PATH := venv/bin/
else
	VENV_PATH :=
endif

pep8:
	$(VENV_PATH)pep8 --max-line-length=119 --show-source  falstart/

pyflakes:
	$(VENV_PATH)pylama -l pyflakes falstart/

lint:
	make pep8
	make pyflakes

test:
	$(VENV_PATH)nosetests ./tests/  --with-specplugin

ci_test:
	make test
	make lint

pypi:
	python setup.py sdist bdist_wheel upload
