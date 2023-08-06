def init_db():
    f = open('db_config.json', 'w')

    template = '{' + ', '.join([f'"{config_key}": null' for config_key in _config_keys]) + '}'

    f.write(template)

    f.close()


def upgrade_db():
    import os
    import json
    from sqlalchemy import engine
    from alembic.config import Config
    from alembic.command import upgrade

    with open('db_config.json') as config_file:
        config_data = json.load(config_file)

        config = {}
        for key in _config_keys:
            if key in config_data and config_data[key]:
                config[key] = config_data[key]

    if 'db_uri' not in config.keys():
        print('no db_uri supported.')
        return

    ini_file_path = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0], 'alembic.ini')
    config_object = Config(ini_file_path)
    config_object.set_main_option('sqlalchemy.url', config['db_uri'])

    with engine.begin() as connection:
        config_object.attributes['connection'] = connection

    upgrade(config_object, 'head')


_config_keys = [
    'db_uri',
]
