import os
import sys
import string
import random

import fabric
from fabric.api import run, sudo, cd, put


fabric.state.env.colorize_errors = True
# fabric.state.output['stdout'] = False

sys.path.insert(0, os.path.dirname(__file__))

VARS = dict(
    base_path=os.getcwd(),
    templates_dir=os.path.join(os.path.dirname(__file__), 'templates')
)


def str_random(size=9, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def render_template(template_name, remote_name):
    fabric.contrib.files.upload_template(
        template_name, remote_name,
        context=VARS, use_jinja=True,
        backup=False, use_sudo=False, template_dir=VARS['templates_dir']
    )


def common():
    read_data()
    start_box()


def read_data():
    from settings import settings
    VARS.update(settings)

    if 'proj_ip' not in VARS:
        VARS['proj_ip'] = raw_input('project ip: ')

    if 'proj_name' not in VARS:
        VARS['proj_name'] = raw_input('project name: ')

    if 'box_name' not in VARS:
        VARS['box_name'] = raw_input('box name: ')

    if 'db_pass' not in VARS:
        VARS['db_pass'] = str_random()

    VARS['root_dir'] = os.path.join(VARS['base_path'], VARS['proj_name'])


def start_box():
    """ Create Vagrant file and up virtual machine """
    run('mkdir -p {root_dir}'.format(**VARS))
    with cd(VARS['root_dir']):
        render_template('Vagrantfile.j2', 'Vagrantfile')
        render_template('Makefile.j2', 'Makefile')
        # make provisioning folder
        run('mkdir -p provision')
        render_template('provision_fabfile.j2', 'provision/fabric_provisioner.py')
        # copy templates for vagrant fabric render
        path = os.path.join(VARS['templates_dir'], 'vagrant_templates')
        remote_path = 'provision/templates'
        run('mkdir -p {}'.format('provision/templates'))
        put(path, remote_path)
        # run vagrant up
        run('vagrant up')


def reprovision():
    read_data()
    with cd(VARS['root_dir']):
        run('vagrant provision')


def rmproj():
    """ Remove project """
    read_data()
    with cd(VARS['root_dir']):
        run('vagrant destroy')

    run('rm {root_dir} -rf'.format(**VARS))
