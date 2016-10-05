

"""
Since this line until the end of file is helpfull code which should be
automatically removed at the end of deployment box. If occurred errors
and boxing has not made a complete build. It is necessary to correct
the errors and manually delete the code.
"""

def app():
    """ Run application tasks """
    with cd(VARS['root_dir']):
        # Create venv and install requirements
        run('pyvenv-{{ pyenv_version }} {venv_path}'.format(**VARS))
        # make wheels for python packages
        run('{venv_path}/bin/pip install -U pip wheel'.format(**VARS))
        run('mkdir -p wheels')
        run('{venv_path}/bin/pip wheel -w wheels/ -r requirements-remote.txt --pre'.format(**VARS))
        # Install required python packages with pip from wheels archive
        run('make wheel_install')
        # run app tasks for devserver start
        start_app()
        # Copy settings local
        run('cd {project_name} && cp settings_local.py.example settings_local.py'.format(**VARS))


def start_app():
    """ start dj app """
    with fabric.context_managers.settings(warn_only=True):
        run('{venv_path}/bin/django-admin startproject {project_name} .'.format(**VARS))

    with open('{project_name}/settings.py'.format(**VARS), 'r') as settings_file:
        settings = settings_file.read()

    # make replacements
    settings = settings.replace(
        dedent(
        '''\
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        '''),
        dedent(
        '''\
            import sys
            BASE_DIR = os.path.dirname(os.path.dirname(__file__))

            if __name__ in ['settings', '{project_name}.settings']:
                sys.path.insert(0, os.path.join(BASE_DIR, '{project_name}'))
        '''.format(**VARS)
        )
    )
{% if POSTGRES %}
    settings = settings.replace('''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
''', '''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '%(db_name)s',
        'USER': '%(db_user)s',
        'PASSWORD': '%(db_password)s',
        'HOST': '127.0.0.1',
    }
}''' % VARS)
{% endif %}
    if 'STATIC_ROOT' not in settings:
        settings = settings.replace('''
STATIC_URL = '/static/'
''', '''
TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverRunner'

STATIC_URL = '/static/'
STATIC_ROOT = '%(project_name)s/static'
{% if CELERY %}

# celery settings
broker_connection_link = {% if REDIS %}'redis://localhost:6379/0'{% else %}'amqp://guest:guest@localhost:5672//'{% endif %}

BROKER_URL = CELERY_RESULT_BACKEND = broker_connection_link
CELERY_ACCEPT_CONTENT = ['json', ]
{% endif %}

try:
    from settings_local import *  # noqa
except ImportError:
    pass
''' % VARS)

    with open('{project_name}/settings.py'.format(**VARS), 'w') as settings_file:
        settings_file.write(settings)
{% endif %}
{% if CELERY %}
    with open('{project_name}/__init__.py'.format(**VARS), 'w') as init_file:
        init_file.write('''# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app  # noqa
''')
{% endif %}