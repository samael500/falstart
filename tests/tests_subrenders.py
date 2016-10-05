from . import FalstartTestCase


class PartialRenderTestCase(FalstartTestCase):

    """ Check is correct rendered includes to provision fabfile """

    def test_db_render_sqlite(self):
        """ Should check the db provisioning correct when sqlite """
        template_name = 'includes/database.j2'
        context = {'POSTGRES': False}
        self.assertEqualRender(template_name, context, 'db_sqlite.txt')

    def test_db_render_postgres(self):
        """ Should check the db provisioning correct when postgres """
        template_name = 'includes/database.j2'
        context = {'POSTGRES': True}
        self.assertEqualRender(template_name, context, 'db_postgres.txt')
