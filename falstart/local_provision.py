import json
import os
import shutil
import subprocess

from textwrap import dedent
from jinja2 import Environment, FileSystemLoader


VARS = dict(
    init_app=True,
    custom_box=False,
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
    falstart_print('run: "{}"'.format(command))
    subprocess.check_call(command, shell=True)


def put(src, dst):
    falstart_print('copy: "{}" > "{}"'.format(src, dst))
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def mkdir(path):
    falstart_print('make dir: "{}"'.format(path))
    try:
        os.makedirs(path)
    except OSError:
        pass


def render_template(template_name, remote_name):
    """ Render wrapper for simplify touch rendered template into target """
    if os.path.dirname(remote_name):
        mkdir(os.path.dirname(remote_name))
    # load jinja template
    jinja_env = Environment(loader=FileSystemLoader(VARS['templates_dir']))
    template = jinja_env.get_template(template_name)
    # write to remote file
    falstart_print('render "{}" > "{}"'.format(template_name, remote_name))
    with open(remote_name, 'w') as target_file:
        target_file.write(template.render(**VARS))


def common(taskname, root_dir, config=None):
    """ Run all common tasks """
    root_dir = os.path.join(os.getcwd(), root_dir)
    mkdir(root_dir)
    os.chdir(root_dir)
    # update configs
    if config is None:
        VARS.update(json.load(open('.falstart.json', 'r')))
    else:
        json.dump(config, open('.falstart.json', 'w'))
        VARS.update(config)
    VARS['root_dir'] = root_dir
    globals()[taskname]()


def start_box():
    """ Create Vagrant file and up virtual machine """
    # render templates for vagrant up
    render_template('Vagrantfile.j2', 'Vagrantfile')
    render_template('Makefile.j2', 'Makefile')
    run('chmod +x Makefile')
    # make provisioning folder
    mkdir('provision')
    render_template('provision_fabfile.j2', 'provision/fabric_provisioner.py')
    render_template('requirements.j2', 'requirements.txt')
    render_template('requirements.j2', 'requirements-remote.txt')
    render_template('lintrc.j2', '.lintrc')
    render_template('coveragerc.j2', '.coveragerc')
    render_template('py_codes/settings_local.j2', '{proj_name}/settings_local.py.example'.format(**VARS))
    if VARS.get('CELERY'):
        render_template('py_codes/celery.j2', '{proj_name}/celery.py'.format(**VARS))
    # copy templates for vagrant fabric render
    put(os.path.join(VARS['templates_dir'], 'vagrant_templates'), 'provision/templates')
    try:
        # run vagrant up
        run('vagrant up')
    except:
        falstart_print('Error occurred when up the vagrant machine.', error=True)
        falstart_print('You can try to manually start the Vagrant.', error=True)

    # replace template
    VARS['init_app'] = False
    render_template('provision_fabfile.j2', 'provision/fabric_provisioner.py')
    # commit changes
    falstart_commit()


def falstart_commit():
    """ Try to commit after box start """
    render_template('gitignore.j2', '.gitignore')
    extra_ignore = dedent('''
        # custom ignore'
        settings_local.py
        .vagrant
        static/
    ''')

    falstart_print('Update .gitignore')
    with open('.gitignore', 'a') as gitignore:
        gitignore.write(extra_ignore)

    for attempt in range(2):
        try:
            run('git add . && git commit -m ":rocket: falstart init commit"')
            break
        except:
            falstart_print('not a git repository', error=True)
            run('git init')


def make_custom_box():
    VARS['custom_box'] = True
    run('vagrant destroy -f')
    # render templates to no provide app and syncfolder
    render_template('Vagrantfile.j2', 'Vagrantfile')
    run('vagrant up')
    for cmd in (
            'sudo dd if=/dev/zero of=/EMPTY bs=1M', 'sudo rm -f /EMPTY',
            'cat /dev/null > ~/.bash_history && history -c'):
        run('vagrant ssh -c "{}"'.format(cmd))
    # make custom box
    run('vagrant package --output ~/{proj_name}.box'.format(**VARS))
    # return template to back
    VARS['custom_box'] = False
    render_template('Vagrantfile.j2', 'Vagrantfile')


def rmproj():
    """ Remove project """
    run('cd {root_dir} && vagrant destroy -f'.format(**VARS))
    run('rm {root_dir} -rf'.format(**VARS))
