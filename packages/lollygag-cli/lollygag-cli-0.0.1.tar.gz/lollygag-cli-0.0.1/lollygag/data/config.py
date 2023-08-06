
import os
import configparser
import errno

class Config():

    _parser = None

    def parser():

        Config._parser = configparser.ConfigParser(allow_no_value=True)

        user_config_dir = os.path.expanduser("~")
        config = configparser.ConfigParser(allow_no_value=True)

        file_path = f'{os.path.expanduser("~")}/.lollygag/lollygag.config'
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        if not os.path.isfile(file_path):
            Config._build_config(file_path)

        Config._parser.read(file_path)

        return Config._parser

    def get_db_path():
        return Config.parser().get('core', 'db_path')
    
    def _build_config(file_path):

        Config._parser.add_section('core')
        Config._parser.set('core', 'db_path',f'sqlite:///{os.path.expanduser("~")}/.lollygag/lollygag.db')

        Config._parser.write(open(file_path, 'w'))