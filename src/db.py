from typing import Union

from pymongo import MongoClient
from config.config import Config

uri = Config.get("mongo", "uri")
print(uri)

# CLIENT = MongoClient(uri)
CLIENT = MongoClient("localhost", 27017)
print(CLIENT)


class DB:
    db = CLIENT["ads-scrapper"]
    collection = db["bama_car"]

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
        res = cls.collection.find({"numbers": None}).limit(length)
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
