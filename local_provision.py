import json
import os
import shutil
import subprocess
import sys

from jinja2 import Environment, FileSystemLoader


VARS = dict(
    init_app=True,
    custome_box=False,
    templates_dir=os.path.join(os.path.dirname(__file__), 'templates')
)


def falstart_print(message, error=False, prefix='[falstart] >'):
    """ Display given message with prefix"""
    bold, red, end = '\033[1m', '\033[31m', '\033[0m'
    print(''.join((
        red if error else '',
        bold, prefix, end,
        red if error else '',
        ' ', message, end,
    )).strip())


def run(command):
    """ wrapper of subprocess check_call fun """
    falstart_print('run "{}"'.format(command))
    subprocess.check_call(command, shell=True)


def put(src, dst):
    falstart_print('copy "{}" > "{}"'.format(src, dst))
    shutil.copytree(src, dst)


def render_template(template_name, remote_name):
    """ Render wrapper for simplify touch rendered template into target """
    if os.path.dirname(remote_name):
        run('mkdir -p {}'.format(os.path.dirname(remote_name)))
    # load jinja template
    jinja_env = Environment(loader=FileSystemLoader(VARS['templates_dir']))
    template = jinja_env.get_template(template_name)
    # write to remote file
    falstart_print('render "{}" > "{}"'.format(template_name, remote_name))
    with open(remote_name, 'w') as target_file:
        target_file.write(template.render(**VARS))


def common(taskname):
    """ Run all common tasks """
    config = json.load(open(os.path.join(os.path.dirname(__file__), 'cfg.json')))
    VARS.update(config)
    globals()[taskname]()


def start_box():
    """ Create Vagrant file and up virtual machine """
    run('mkdir -p {root_dir}'.format(**VARS))
    # chandge working dir to root dir
    os.chdir(VARS['root_dir'])
    # render templates for vagrant up
    render_template('Vagrantfile.j2', 'Vagrantfile')
    render_template('Makefile.j2', 'Makefile')
    run('chmod +x Makefile')
    # make provisioning folder
    run('mkdir -p provision')
    render_template('provision_fabfile.j2', 'provision/fabric_provisioner.py')
    render_template('requirements.j2', 'requirements.txt')
    render_template('requirements.j2', 'requirements-remote.txt')
    render_template('settings_local.j2', '{proj_name}/settings_local.py.example'.format(**VARS))
    if VARS.get('CELERY'):
        render_template('celery.j2', '{proj_name}/celery.py'.format(**VARS))
    # copy templates for vagrant fabric render
    put(os.path.join(VARS['templates_dir'], 'vagrant_templates'), 'provision/templates')
    # run vagrant up
    run('vagrant up')
    # replace template
    VARS['init_app'] = False
    render_template('provision_fabfile.j2', 'provision/fabric_provisioner.py')
    # commit changes
    falstart_commit()


def falstart_commit():
    """ Try to commit after box start """
    os.chdir(VARS['root_dir'])
    run('''echo "
*.py[cod]
__pycache__/
# custome ignore
settings_local.py
.vagrant
var/
static/
" >> .gitignore''')
    for attempt in range(2):
        try:
            run('git add . && git commit -m ":rocket: falstart init commit"')
            break
        except:
            falstart_print('not a git repository', error=True)
            run('git init')


def make_custome_box():
    os.chdir(VARS['root_dir'])

    VARS['custome_box'] = True
    run('vagrant destroy -f')
    # render templates to no provide app and syncfolder
    render_template('Vagrantfile.j2', 'Vagrantfile')
    run('vagrant up')
    for cmd in (
            'sudo dd if=/dev/zero of=/EMPTY bs=1M', 'sudo rm -f /EMPTY',
            'cat /dev/null > ~/.bash_history && history -c'):
        run('vagrant ssh -c {cmd}')
    # make custome box
    run('vagrant package --output ~/{proj_name}.box'.format(**VARS))
    # return template to back
    VARS['custome_box'] = False
    render_template('Vagrantfile.j2', 'Vagrantfile')


def rmproj():
    """ Remove project """
    run('cd {root_dir} && vagrant destroy'.format(**VARS))
    run('rm {root_dir} -rf'.format(**VARS))
