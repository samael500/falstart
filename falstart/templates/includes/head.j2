# vi: syntax=python
import os
import fabric

from inspect import getsource
from textwrap import dedent
from fabric.api import run, sudo, cd

fabric.state.env.colorize_errors = True
fabric.state.output['stdout'] = False

# task const variables
VARS = dict(
    current_user=fabric.state.env.user,

    # project settings
    project_name='{{ proj_name }}',
    user_data=dict(
        username='root',
        email='root@e.co',
        password='123123'
    ),

    # dirs configs
    templates_dir='./provision/templates',
    root_dir='/home/vagrant/proj',
    venv_path='/home/vagrant/venv',
    base_dir='/home/vagrant',

    # nginx config
    http_host='{{ proj_ip }}',
    http_port='80',
{% if POSTGRES %}
    # database config
    db_name='{{ proj_name }}',
    db_password='{{ db_pass }}',
    db_user='{{ db_user }}',
{% endif %}
    # locale conf
    locale='ru_RU',
    encoding='UTF-8',
)


def sentinel(sentinel_name=None):
    def sentinel_wrapp(function):
        hashed_func_name = '_'.join((function.__name__, str(hash(getsource(function)))))

        def wrapped():
            sentinel_path = '/usr/{}'.format(sentinel_name or hashed_func_name)
            if fabric.contrib.files.exists(sentinel_path):
                fabric.utils.warn('skip {}'.format(sentinel_name or hashed_func_name))
                return
            function()
            sudo('touch {}'.format(sentinel_path))
        return wrapped
    return sentinel_wrapp
