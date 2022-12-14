from time import sleep
from src.db import DB
import requests
from fake_useragent import UserAgent

UA = UserAgent()
URL = "https://bama.ir/car"
END_POINT = "api/search"
QUERY_PARAM = "pageIndex"


class AssessAds:
    LIST_ID = DB.get_last_500_ads_code()

    @classmethod
    def assess_data(cls, data: list):
        output = list()
        for obj in data:
            if obj["ads_code"] in cls.LIST_ID:
                continue
            output.append(obj)
            cls._add_id_to_list(obj["ads_code"])
        return output

    @classmethod
    def _add_id_to_list(cls, _id: str):
        cls.LIST_ID.append(_id)
        if len(cls.LIST_ID) > 2000:
            cls.LIST_ID.pop(0)

    @classmethod
    def get_code_without_phone(cls, length):
        res = DB.get_code_without_phone(length)
        return res

    # @classmethod
    # def get_code_without_phone(cls, length):
    #     output = cls.LIST_ID_WITHOUT_PHONE[:length]
    #     del cls.LIST_ID_WITHOUT_PHONE[:length]
    #     return output


def request_data(pages=30):
    ua = UA.random
    for i in range(pages):
        print("index:", i)
        header = {
            "user-agent": ua
        }
        try:
            res = requests.get(f"https://bama.ir/cad/api/search?pageIndex={i}", headers=header)
            if res.status_code != 200:
                raise Exception(f"status code: {res.status_code}")
            yield res.json()
        except Exception as err:
            raise Exception(err)


def request_phone(length: int = 10):
    ua = UA.random
    for ads in AssessAds.get_code_without_phone(length):
        header = {
            "user-agent": ua
        }
        try:
            res = requests.get(f"https://bama.ir/cad/api/detail/{ads.get('ads_code')}/phone", headers=header)
            if res.status_code != 200:
                raise Exception(f"status code: {res.status_code}")
            data = res.json().get("data")
            DB.update_phone_by_ads_code(ads.get('ads_code'), data)
            sleep(1)
        except Exception as err:
            raise Exception(err)


def clean_data(data: list):
    output = list()
    for obj in data:
        dct = {
            "dealer": obj.get("dealer"),
            "detail": obj.get("detail"),
            "images": obj.get("images"),
            "metadata": obj.get("metadata"),
            "price": {"type": obj.get("price", dict()).get("type"),
                      "price": obj.get("price", dict()).get("price")},
            "ads_code": obj.get("detail", dict()).get("code"),
            "phones": None
        }
        output.append(dct)
    return output


def fetch_data(start_msg):
    for res in request_data():
        ads_list: list = res.get('data', dict()).get('ads', list())
        if not ads_list:
            raise Exception("no ads fetch!!")
        ads_list = clean_data(ads_list)
        ads_list = AssessAds.assess_data(ads_list)
        print("data length:", len(ads_list))
        if ads_list:
            DB.insert_many(ads_list)
            request_phone(30)
            continue
        if start_msg == 'loop start':
            break
    request_phone()
    sleep(5)
    return True
