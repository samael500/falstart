from . import FalstartTestCase


class PartialRenderTestCase(FalstartTestCase):

    """ Check is correct rendered includes to provision fabfile """

    def test_db_render_sqlite(self):
        """ Should check the db provisioning correct when sqlite """
        template_name = 'includes/database.j2'
        context = {'POSTGRES': False}
        with open('etalons/db_sqlite.txt') as etalon:
            self.assertEqual(self.render_to_string(template_name, context), etalon.read())

    def test_db_render_postgres(self):
        """ Should check the db provisioning correct when postgres """
        template_name = 'includes/database.j2'
        context = {'POSTGRES': True}
        with open('etalons/db_postgres.txt') as etalon:
            self.assertEqual(self.render_to_string(template_name, context), etalon.read())
