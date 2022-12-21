from time import sleep

import requests
from fake_useragent import UserAgent

from src.db import DB

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
            if obj["id"] in cls.LIST_ID:
                continue
            output.append(obj)
            cls._add_id_to_list(obj["id"])
        return output

    @classmethod
    def _add_id_to_list(cls, _id: str):
        cls.LIST_ID.append(_id)
        if len(cls.LIST_ID) > 2000:
            cls.LIST_ID.pop(0)

    @classmethod
    def get_code_without_phone(cls, length):
        res = DB.get_code_without_phone(length)
        return res if res else list()

    # @classmethod
    # def get_code_without_phone(cls, length):
    #     output = cls.LIST_ID_WITHOUT_PHONE[:length]
    #     del cls.LIST_ID_WITHOUT_PHONE[:length]
    #     return output


def request_data(pages=100):
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
    lst = AssessAds.get_code_without_phone(length)
    for ads in lst:
        header = {
            "user-agent": ua
        }
        try:
            res = requests.get(f"https://bama.ir/cad/api/detail/{ads.get('id')}/phone", headers=header)
            if res.status_code != 200:
                raise Exception(f"status code: {res.status_code}")
            data: dict = res.json().get("data")
            DB.update_phone_by_ads_code(ads.get('id'), data)
            sleep(1)
        except Exception as err:
            raise Exception(err)


class CleanData:
    @classmethod
    def clean_data(cls, data: list):
        output = list()
        for obj in data:
            dct = {
                "link": "https://bama.ir" + obj.get('detail', dict).get('url') if obj.get('detail') else None,
                "id": obj.get('detail', dict()).get('code'),
                "id_str": obj.get('detail', dict()).get('code'),
                "title": obj.get('metadata', dict()).get('title_tag'),
                "text": obj.get('metadata', dict).get('description'),
                "publish_date": obj.get("detail", dict()).get('modified_date'),
                "location": obj.get('detail', dict()).get('location'),
                "user": cls.format_user(obj.get('dealer')),
                "media": cls.format_image(obj.get('images')),
                "specs": cls.format_specs(obj.get('detail')),
                "price_info": cls.format_price_info(obj.get('price')),
                "numbers": None,
            }
            output.append(dct)
        return output

    @classmethod
    def format_user(cls, data: dict):
        if not data:
            return None
        output = {
            'id': data.get('id'),
            'is_auto_shop': True if data.get('type') == "نمایشگاه" else False,
            'name': data.get('name'),
            'profile_image_url': data.get('logo'),
            'url': "https://bama.ir" + data.get('link') if data.get('link') else None,
            "location": data.get('address'),
            "ad_count": data.get('ad_count')
        }
        return output

    @classmethod
    def format_image(cls, data: list):
        if not data:
            return []
        output = {'images': list()}
        for obj in data:
            dct = {'main_url': obj.get('large')}
            output['images'].append(dct)
        return output

    @classmethod
    def format_specs(cls, data: dict):
        if not data:
            return None
        trim: str = data.get('trim')
        trim = trim.split('|')[0]
        output = {
            "model": data.get('title'),
            "sub_model": trim,
            "production_year": data.get('year'),
            "kilometers": data.get('mileage'),
            "gearbox_type": data.get('transmission'),
            "fuel_type": data.get('fuel'),
            "color": data.get('color'),
            "body_color": data.get('body_color'),
            "inside_color": data.get('inside_color'),
            "body_condition": data.get('body_status'),
            "body_type": data.get('body_type'),
        }
        return output

    @classmethod
    def format_price_info(cls, data: dict):
        if not data:
            return None
        _type = None
        if data.get("type") == "lumpsum":
            _type = "cash"
        elif data.get("type") == "installment":
            _type = "installments"
        else:
            _type = "cash"
        price: str = data.get("price")
        price = price.replace(",", "")
        price: int = int(price)
        price_eventually = price if price > 0 else None
        output = {
            "type": _type,
            "price": price_eventually,
            "prepayment": data.get("prepayment"),
            "payment": data.get("payment"),
            "prepayment_primary": data.get("prepayment_primary"),
            "prepayment_secondary": data.get("prepayment_secondary"),
            "payment_primary": data.get("payment_primary"),
            "month_number": data.get("month_number"),
            "installments": data.get("installments"),
            "delivery_days": data.get("delivery_days"),
        }
        return output


def fetch_data(start_msg):
    for res in request_data():
        ads_list: list = res.get('data', dict()).get('ads', list())
        if not ads_list:
            raise Exception("no ads fetch!!")
        ads_list = CleanData.clean_data(ads_list)
        ads_list = AssessAds.assess_data(ads_list)
        print("data length:", len(ads_list))
        if ads_list:
            DB.insert_many(ads_list)
            request_phone(30)
            continue
        if start_msg == 'loop start':
            break
    request_phone(30)
    sleep(5)
    return True
