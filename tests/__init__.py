import os
from unittest import TestCase
from difflib import ndiff
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class FalstartTestCase(TestCase):

    """ Abstract base Test Case for Falstart. """

    def render_to_string(self, template_name, context, template_dir=None):
        """ Render template to string """
        template_dir = template_dir or os.path.join(BASE_DIR, 'falstart', 'templates')
        # load jinja template
        jinja_env = Environment(loader=FileSystemLoader(template_dir))
        template = jinja_env.get_template(template_name)
        # write to remote file
        return template.render(**context)

    def assertEqualRender(self, template_name, context, etalon_name):
        """ Open etalon file and check render correct """
        with open(os.path.join(BASE_DIR, 'tests', 'etalons', etalon_name)) as etalon:
            rendered = self.render_to_string(template_name, context)
            corrected = etalon.read()
            try:
                self.assertEqual(corrected, rendered)
            except:
                print "Etalon: {}".format(etalon_name)
                for row in ndiff(rendered.split('\n'), corrected.split('\n')):
                    print row
                assert False
