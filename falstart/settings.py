VARS = dict(
    # vagrant conf
    proj_ip='10.1.1.123',
    box_name='debian/jessie64',
    vagrant_memory=2048,
    vagrant_cpus=2,

    # include / declude config
    POSTGRES=True,
    CELERY=False,
    REDIS=False,

    # project settings
    proj_name=None,
    root_dir=None,

    # database config
    db_name=None,
    db_pass=None,
    db_user=None,

    # locale conf
    locale='ru_RU',
    encoding='UTF-8',

    # python version
    dj_version='1.9.5',
    py_version='3.5.1',
    pyenv_version=None,

    # extra configs
    SENTRY=False,
)
