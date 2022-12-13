import configparser
import json


class Configer:

    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read('config/config.ini', encoding='utf-8')

    def get(self, *args, _type="str"):
        try:
            self.parser.sections()
            if _type == "int":
                return self.parser.getint(*args)

            if _type == "str":
                return self.parser.get(*args)

            if _type == "float":
                return self.parser.getfloat(*args)

            if _type == "boolean":
                return self.parser.getboolean(*args)

            if _type == "list":
                return json.loads(self.parser.get(*args))
            else:
                print(f"you entered wrong value:{_type} to type. please enter these value: int | str | float | boolean")

        except Exception as e:
            print("config.py --> def get_config -->", e, ",args=>", *args)
