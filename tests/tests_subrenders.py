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

    def test_render_app(self):
        """ Should check the app provisioning correct when no celery """
        template_name = 'includes/app.j2'
        context = {'pyenv_version': 3.1415, 'CELERY': False}
        self.assertEqualRender(template_name, context, 'app.txt')

    def test_render_app_celery(self):
        """ Should check the app provisioning correct when celery """
        template_name = 'includes/app.j2'
        context = {'pyenv_version': 3.1415, 'CELERY': True}
        self.assertEqualRender(template_name, context, 'app_celery.txt')

    def test_render_app_init(self):
        """ Should check the app init provisioning correct when celery and pg """
        template_name = 'includes/app_init.j2'
        context = {
            'pyenv_version': 3.1415, 'CELERY': True, 'POSTGRES': True,
            'db_name': 'test_db_name', 'db_user': 'test_db_user', 'db_pass': 'test_db_pass'}
        self.assertEqualRender(template_name, context, 'app_init.txt')

    def test_render_app_init_no_celery(self):
        """ Should check the app init provisioning correct when no celery and pg """
        template_name = 'includes/app_init.j2'
        context = {
            'pyenv_version': 3.1415, 'CELERY': False, 'POSTGRES': True,
            'db_name': 'test_db_name', 'db_user': 'test_db_user', 'db_pass': 'test_db_pass'}
        self.assertEqualRender(template_name, context, 'app_init_no_celery.txt')

    def test_render_app_init_no_celery_no_pg(self):
        """ Should check the app init provisioning correct when no celery and no pg """
        template_name = 'includes/app_init.j2'
        context = {
            'pyenv_version': 3.1415, 'CELERY': False, 'POSTGRES': False,
            'db_name': 'test_db_name', 'db_user': 'test_db_user', 'db_pass': 'test_db_pass'}
        self.assertEqualRender(template_name, context, 'app_init_no_celery_no_pg.txt')

    def test_render_app_init_no_pg(self):
        """ Should check the app init provisioning correct when celery and no pg """
        template_name = 'includes/app_init.j2'
        context = {
            'pyenv_version': 3.1415, 'CELERY': True, 'POSTGRES': False,
            'db_name': 'test_db_name', 'db_user': 'test_db_user', 'db_pass': 'test_db_pass'}
        self.assertEqualRender(template_name, context, 'app_init_no_pg.txt')

    def test_render_common_tasks(self):
        """ Should check the commont tasks correct """
        template_name = 'includes/common.j2'
        context = {'py_version': 3.1415}
        self.assertEqualRender(template_name, context, 'common.txt')

    def test_render_common_redis_tasks(self):
        """ Should check the commont tasks correct when redis """
        template_name = 'includes/common.j2'
        context = {'py_version': 3.1415, 'REDIS': True, 'CELERY': True}
        self.assertEqualRender(template_name, context, 'common_redis.txt')

    def test_render_common_ampq_tasks(self):
        """ Should check the commont tasks correct when rabbitmq """
        template_name = 'includes/common.j2'
        context = {'py_version': 3.1415, 'CELERY': True}
        self.assertEqualRender(template_name, context, 'common_ampq.txt')

    def test_db_render_settings_local(self):
        """ Should check the settings local correct render """
        template_name = 'py_codes/settings_local.j2'
        context = {}
        self.assertEqualRender(template_name, context, 'settings_local.txt')

    def test_db_render_settings_local_postgres(self):
        """ Should check the settings local correct render with pg """
        template_name = 'py_codes/settings_local.j2'
        context = {'POSTGRES': True, 'proj_name': 'test_proj', 'db_user': 'test_user', 'db_pass': 'test_pass'}
        self.assertEqualRender(template_name, context, 'settings_local_postgres.txt')

    def test_db_render_settings_local_sentry(self):
        """ Should check the settings local correct render with sentry """
        template_name = 'py_codes/settings_local.j2'
        context = {
            'SENTRY': True, 'POSTGRES': True, 'proj_name': 'test_proj',
            'db_user': 'test_user', 'db_pass': 'test_pass'}
        self.assertEqualRender(template_name, context, 'settings_local_sentry.txt')

    def test_db_render_settings_local_sentry_celery(self):
        """ Should check the settings local correct render with sentry and celery """
        template_name = 'py_codes/settings_local.j2'
        context = {
            'SENTRY': True, 'POSTGRES': True, 'proj_name': 'test_proj', 'CELERY': True,
            'db_user': 'test_user', 'db_pass': 'test_pass'}
        self.assertEqualRender(template_name, context, 'settings_local_sentry_celery.txt')
