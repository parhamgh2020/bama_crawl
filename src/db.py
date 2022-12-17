from typing import Union

from pymongo import MongoClient
from config.config import Configer

configer = Configer()
host = configer.get("mongo", "host", _type="str")
port = configer.get("mongo", "port", _type="int")

CLIENT = MongoClient(host, port)


class DB:
    db = CLIENT["db1"]
    collection = db["col1"]

    @classmethod
    def insert(cls, data: dict):
        pass

    @classmethod
    def insert_many(cls, data: list):
        if data:
            res = cls.collection.insert_many(data, ordered=True)
            print("insert mongo:", res.acknowledged)

    @classmethod
    def get_by_ads_id(cls, _id):
        pass

    @classmethod
    def update_phone_by_ads_code(cls, ads_code: str, data: dict):
        phones: dict = cls._format_numbers(data)
        res = cls.collection.update_many({"id": ads_code}, {"$set": {"numbers": phones}})
        print("update phones:", res.acknowledged, ", ads_code:", ads_code)

    @classmethod
    def get_code_without_phone(cls, length):
        res = cls.collection.find({"phones": None}).limit(length)
        return res

    @classmethod
    def get_last_500_ads_code(cls):
        res = cls.collection.find().sort('_id', -1).limit(500)
        res = [obj.get('ads_code') for obj in res]
        return res

    @staticmethod
    def _format_numbers(data: dict) -> Union[dict, None]:
        if not data:
            return None
        output = {
            'phones': list(),
            'mobiles': list(),
        }

        def _get_format(number):
            format_num = number.replace('(', '')
            format_num = format_num.replace(')', '')
            format_num = format_num.split(' ')
            format_num = "".join(format_num)
            return format_num

        phones = data.get('phone') if data.get('phone') else list()
        for num in phones:
            num = _get_format(num)
            output['phones'].append(num)
        mobiles = data.get('mobile') if data.get('mobile') else list()
        for num in mobiles:
            num = _get_format(num)
            output['mobiles'].append(num)
        return output
