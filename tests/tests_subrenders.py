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

    def test_db_render_app(self):
        """ Should check the app provisioning correct when no celery """
        template_name = 'includes/app.j2'
        context = {'pyenv_version': 3.1415, 'CELERY': False}
        self.assertEqualRender(template_name, context, 'app.txt')

    def test_db_render_app_celery(self):
        """ Should check the app provisioning correct when celery """
        template_name = 'includes/app.j2'
        context = {'pyenv_version': 3.1415, 'CELERY': True}
        self.assertEqualRender(template_name, context, 'app_celery.txt')

    def test_db_render_app_init(self):
        """ Should check the app init provisioning correct when celery and pg """
        template_name = 'includes/app_init.j2'
        context = {'pyenv_version': 3.1415, 'CELERY': True, 'POSTGRES': True}
        self.assertEqualRender(template_name, context, 'app_init.txt')
