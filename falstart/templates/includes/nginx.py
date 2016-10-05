def nginx():
    """ Install and configure nginx tasks """
    nginx_install()
    # create nginx config file for project
    fabric.contrib.files.upload_template(
        'nginx-host.j2', '/etc/nginx/sites-available/{project_name}'.format(**VARS),
        context=VARS, use_jinja=True, backup=False, use_sudo=True, template_dir=VARS['templates_dir'])
    # make s-link to enabled sites
    sudo('ln -sf /etc/nginx/sites-available/{project_name} /etc/nginx/sites-enabled/{project_name}'.format(**VARS))
    # restart nginx
    sudo('service nginx restart')


@sentinel()
def nginx_install():
    """ Install nginx """
    # install nginx
    sudo('apt-get -y install nginx')
