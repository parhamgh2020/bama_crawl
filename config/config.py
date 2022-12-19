import configparser


class Config:
    config = configparser.ConfigParser(interpolation=None)
    config.read('config/config.ini')

    @classmethod
    def get(cls, *args):
        return cls.config.get(*args)

    @classmethod
    def get_bool(cls, *args):
        return cls.config.getboolean(*args)
