from jinja2 import Environment, FileSystemLoader

def render_to_string(template_name):
    """ Render template to string """
    # load jinja template
    jinja_env = Environment(loader=FileSystemLoader(VARS['templates_dir']))
    template = jinja_env.get_template(template_name)
    # write to remote file
    return target_file.write(template.render(**VARS))

