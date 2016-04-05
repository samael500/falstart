import os
import json

import fabric
from fabric.api import run, sudo, cd, put, local, lcd
from jinja2 import Environment, FileSystemLoader


fabric.state.env.colorize_errors = True
# fabric.state.output['stdout'] = False


VARS = dict(
    init_app=True,
    custome_box=False,
    templates_dir=os.path.join(os.path.dirname(__file__), 'templates')
)


def render_template(template_name, remote_name):
    """ Render wrapper for simplify touch rendered template into target """
    if os.path.dirname(remote_name):
        local('mkdir -p {}'.format(os.path.dirname(remote_name)))
    loader = FileSystemLoader(VARS['templates_dir'])
    jinja_env = Environment(loader=loader)
    template = jinja_env.get_template(template_name)
    template.render(**VARS)
    with open(os.path.join(fabric.state.env.lcwd, remote_name), 'w') as target_file:
        target_file.write(template.render(**VARS))


def common(taskname):
    """ Run all common tasks """
    config = json.load(open(os.path.join(os.path.dirname(__file__), 'cfg.json')))
    VARS.update(config)
    fabric.tasks.execute(taskname)


def start_box():
    """ Create Vagrant file and up virtual machine """
    local('mkdir -p {root_dir}'.format(**VARS))
    with lcd(VARS['root_dir']), cd(VARS['root_dir']):
        render_template('Vagrantfile.j2', 'Vagrantfile')
        render_template('Makefile.j2', 'Makefile')
        local('chmod +x Makefile')
        # make provisioning folder
        local('mkdir -p provision')
        render_template('provision_fabfile.j2', 'provision/fabric_provisioner.py')
        render_template('requirements.j2', 'requirements.txt')
        render_template('requirements.j2', 'requirements-remote.txt')
        render_template('settings_local.j2', '{proj_name}/settings_local.py.example'.format(**VARS))
        if VARS.get('CELERY'):
            render_template('celery.j2', '{proj_name}/celery.py'.format(**VARS))
        # copy templates for vagrant fabric render
        path = os.path.join(VARS['templates_dir'], 'vagrant_templates')
        local('mkdir -p {}'.format('provision/templates'))
        put(path, 'provision')
        local('rm -rf provision/templates && mv -f provision/vagrant_templates provision/templates')
        # run vagrant up
        local('vagrant up')
        # replace template
        VARS['init_app'] = False
        render_template('provision_fabfile.j2', 'provision/fabric_provisioner.py')
    fabric.tasks.execute('falstart_commit')


def falstart_commit():
    """ Try to commit after box start """
    with lcd(VARS['root_dir']), fabric.context_managers.settings(warn_only=True):
        local('''echo "
# custome ignore
settings_local.py
.vagrant
var/
static/
" >> .gitignore''')
        local('git add . && git commit -m ":rocket: falstart init commit"')


def make_custome_box():
    with lcd(VARS['root_dir']):
        VARS['custome_box'] = True
        local('vagrant destroy -f')
        # render templates to no provide app and syncfolder
        render_template('Vagrantfile.j2', 'Vagrantfile')
        local('vagrant up')
        for cmd in (
                'sudo dd if=/dev/zero of=/EMPTY bs=1M', 'sudo rm -f /EMPTY',
                'cat /dev/null > ~/.bash_history && history -c'):
            local('vagrant ssh -c {cmd}')
        # make custome box
        local('vagrant package --output ~/{proj_name}.box'.format(**VARS))
        # return template to back
        VARS['custome_box'] = False
        render_template('Vagrantfile.j2', 'Vagrantfile')


def rmproj():
    """ Remove project """
    with lcd(VARS['root_dir']):
        local('vagrant destroy')

    local('rm {root_dir} -rf'.format(**VARS))
