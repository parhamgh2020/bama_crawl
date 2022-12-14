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
    def update_phone_by_ads_code(cls, ads_code: str, data: list):
        res = cls.collection.update_many({"ads_code": ads_code}, {"$set": {"phones": data}})
        print("update phone:", res.acknowledged, ", ads_code:", ads_code)

    @classmethod
    def get_code_without_phone(cls, length):
        res = cls.collection.find({"phones": None}).limit(length)
        return res

    @classmethod
    def get_last_500_ads_code(cls):
        res = cls.collection.find().sort('_id', -1).limit(500)
        res = [obj.get('ads_code') for obj in res]
        return res
