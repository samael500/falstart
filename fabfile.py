import os
import sys
import fabric

from fabric.api import run, sudo, cd


fabric.state.env.colorize_errors = True
# fabric.state.output['stdout'] = False

sys.path.insert(0, os.path.dirname(__file__))

VARS = dict(
    base_path=os.getcwd(),
    templates_dir=os.path.join(os.path.dirname(__file__), 'templates')
)

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

    VARS['root_dir'] = os.path.join(VARS['base_path'], VARS['proj_name'])


def start_box():
    """ Create Vagrant file and up virtual machine """
    run('mkdir -p {root_dir}'.format(**VARS))
    with cd(VARS['root_dir']):
        render_template('Vagrantfile.j2', 'Vagrantfile')
        run('vagrant up')

def rmproj():
    read_data()
    run('rm {root_dir} -rf'.format(**VARS))
