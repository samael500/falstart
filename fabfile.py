import os
import json

import fabric
from fabric.api import run, sudo, cd, put


fabric.state.env.colorize_errors = True
# fabric.state.output['stdout'] = False


VARS = dict(
    init_app=True,
    templates_dir=os.path.join(os.path.dirname(__file__), 'templates')
)


def render_template(template_name, remote_name):
    """ Render wrapper for simplify touch rendered template into target """
    if os.path.dirname(remote_name):
        run('mkdir -p {}'.format(os.path.dirname(remote_name)))
    fabric.contrib.files.upload_template(
        template_name, remote_name,
        context=VARS, use_jinja=True,
        backup=False, use_sudo=False, template_dir=VARS['templates_dir']
    )


def common(taskname):
    """ Run all common tasks """
    config = json.load(open(os.path.join(os.path.dirname(__file__), 'cfg.json')))
    VARS.update(config)
    fabric.tasks.execute(taskname)


def start_box():
    """ Create Vagrant file and up virtual machine """
    run('mkdir -p {root_dir}'.format(**VARS))
    with cd(VARS['root_dir']):
        render_template('Vagrantfile.jinja', 'Vagrantfile')
        render_template('Makefile.jinja', 'Makefile')
        run('chmod +x Makefile')
        # make provisioning folder
        run('mkdir -p provision')
        render_template('provision_fabfile.jinja', 'provision/fabric_provisioner.py')
        render_template('requirements.jinja', 'requirements.txt')
        render_template('requirements.jinja', 'requirements-remote.txt')
        render_template('settings_local.jinja', '{proj_name}/settings_local.py.example'.format(**VARS))
        if VARS.get('CELERY'):
            render_template('celery.jinja', '{proj_name}/celery.py'.format(**VARS))
        # copy templates for vagrant fabric render
        path = os.path.join(VARS['templates_dir'], 'vagrant_templates')
        run('mkdir -p {}'.format('provision/templates'))
        put(path, 'provision')
        run('rm -rf provision/templates && mv -f provision/vagrant_templates provision/templates')
        # run vagrant up
        run('vagrant up')
        # replace template
        VARS['init_app'] = False
        render_template('provision_fabfile.jinja', 'provision/fabric_provisioner.py')


def reprovision():
    with cd(VARS['root_dir']):
        run('vagrant provision')


def rmproj():
    """ Remove project """
    with cd(VARS['root_dir']):
        run('vagrant destroy')

    run('rm {root_dir} -rf'.format(**VARS))
