import os
from unittest import TestCase
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class FalstartTestCase(TestCase):

    """ Abstract base Test Case for Falstart. """

    def render_to_string(template_name, context, template_dir=None):
        """ Render template to string """
        template_dir = template_dir or os.path.join(BASE_DIR, 'falstart', 'templates')
        # load jinja template
        jinja_env = Environment(loader=FileSystemLoader(template_dir))
        template = jinja_env.get_template(template_name)
        # write to remote file
        return target_file.write(template.render(**context))
