import json
import traceback
from time import sleep
from typing import Union

import requests
from fake_useragent import UserAgent
from random import choice
from src.db import DB
from config.config import Config

UA = UserAgent()
URL = "https://bama.ir/car"
END_POINT = "api/search"
QUERY_PARAM = "pageIndex"

sleep_time = 2
max_sleep = 60 * 5
step_increase_sleep = 60
step_decrease_sleep = 5

header = {
    # ":authority": "bama.ir",
    # ":method": "GET",
    # ":path": "/cad/api/detail/7WDgqaMe/phone",
    # ":scheme": "https",
    "accept": Config.get("header", "accept"),
    "accept-encoding": Config.get("header", "accept-encoding"),
    "accept-language": Config.get("header", "accept-language"),
    "cookie": Config.get("header", "cookie"),
    "referer": Config.get("header", "referer"),
    "sec-ch-ua": Config.get("header", "sec-ch-ua"),
    "sec-ch-ua-mobile": Config.get("header", "sec-ch-ua-mobile"),
    "sec-ch-ua-platform": Config.get("header", "sec-ch-ua-platform"),
    "sec-fetch-dest": Config.get("header", "sec-fetch-dest"),
    "sec-fetch-mode": Config.get("header", "sec-fetch-mode"),
    "sec-fetch-site": Config.get("header", "sec-fetch-site"),
    "sec-gpc": Config.get("header", "sec-gpc"),
    "traceparent": Config.get("header", "traceparent"),
    "user-agent": Config.get("header", "user-agent"),
}

IPs: list = json.loads(Config.get("proxy", "proxies"))
public_id = Config.get_bool("proxy", "use_public_ip")


class Proxies:

    def __init__(self, ips_list, is_contained_public):
        self.lst = ips_list
        self.index = 0
        if is_contained_public:
            ips_list.append(None)

    def get_proxy(self):
        if self.index == len(self.lst):
            self.index = 0
        ip = self.lst[self.index]
        self.index += 1
        return {
            'http': ip,
            "https": ip,
        }


proxies = Proxies(IPs, public_id)


def send_request(url, proxy=None) -> Union[int, dict]:
    """
    request to bama site
    if proxy is not set then proxy will be set automatically
    if proxy is not set then status code 403 will handle
    :param url: url can be car detail url or phone url
    :param proxy:
    :return: result
    """
    if not proxy:
        _proxy = proxies.get_proxy()
    else:
        _proxy = proxy
    print("proxy:", _proxy['http'] if _proxy['http'] else "public id")
    try:
        res = requests.get(url,
                           headers=header,
                           proxies=_proxy,
                           timeout=5)
    except Exception as err:
        print(f"connection problem: {type(err)}")
        return 500
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 403:
        print("status code:", res.status_code)
        if not proxy:
            proxy = proxies.get_proxy()
            res = send_request(url, proxy)
            return res
        return res.status_code
    else:
        print("status code:", res.status_code)
        return res.status_code


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


def request_data(pages=30):
    for i in range(pages):
        print("index:", i)
        try:
            global sleep_time
            print("sleep:", sleep_time, "seconds")
            sleep(sleep_time)
            res = send_request(f"https://bama.ir/cad/api/search?pageIndex={i}")
            if res == 403:
                if sleep_time < max_sleep:
                    sleep_time += step_increase_sleep
            elif res != 200 and isinstance(res, int):
                print("no action")
            else:
                if sleep_time > 2:
                    sleep_time -= step_decrease_sleep if sleep_time - step_decrease_sleep > 2 else 2
                yield res
        except Exception as err:
            raise Exception(err)


def request_phone(length: int = 10):
    lst = AssessAds.get_code_without_phone(length)
    for ads in lst:
        try:
            global sleep_time
            print("sleep:", sleep_time, "seconds")
            sleep(sleep_time)
            proxy = proxies.get_proxy()
            res = send_request(f"https://bama.ir/cad/api/detail/{ads.get('id')}/phone", proxy)
            if res == 403:
                if sleep_time < max_sleep:
                    sleep_time += step_increase_sleep
            elif res != 200:
                if res == 400:
                    data = {"phone": None, "mobile": None}
                    DB.update_phone_by_ads_code(ads.get('id'), data)
            else:
                if sleep_time > 2:
                    sleep_time -= step_decrease_sleep if sleep_time - step_decrease_sleep > 2 else 2
                data: dict = res.get("data")
                DB.update_phone_by_ads_code(ads.get('id'), data)
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
    request_phone()
    return True
