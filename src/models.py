from datetime import datetime
from typing import Union, List, Literal
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError


class PriceInfo(BaseModel):
    type: Literal['نقدی', "اقساطی"]
    price: Union[int, None]


class Media(BaseModel):
    images: List[dict]  # main_url:


class Phones(BaseModel):
    phones: List[str]
    mobiles: List[str]


class User(BaseModel):
    id: Union[int, str]
    is_auto_shop: bool
    name: str
    profile_image_url: str  # logo
    url: str  # url
    location: str  # address
    ad_count: int


class Specs(BaseModel):
    model: str  # title
    sub_model: str  # trim
    production_year: str  # year
    kilometers: str  # mileage
    gearbox_type: str  # transmission
    fuel_type: str  # fuel
    color: str
    body_color: str
    inside_color: str
    body_condition: str  # body_status
    body_type: str


class AdvertiseModel(BaseModel):
    link: str
    id: Union[str, int]
    id_str: str
    title: str
    text: str  # metadata.description
    publish_date: str  # modified_date: datetime
    location: str
    user: User
    media: Media
    specs: Specs
    price_info: PriceInfo
    numbers: Phones


"""
bama_data = {"_id": {"$oid": "63984190f29d56f3e2123270"},
             "dealer": {"id": 289,
                        "type": "نمایشگاه",
                        "name": "کرمان موتور کد 1762",
                        "logo": "https://cdn.bama.ir/uploads/BamaImages/Corporations/corporation_637109658897068266.png",
                        "link": "/dealer/289",
                        "address": "تهران، خیابان 17 شهریور، پایین تر از محلاتی (آهنگ)، نرسیده به بلوار قیام",
                        "ad_count": 33},
             "detail": {"type": "car",
                        "code": "qj73rRIf",
                        "rank": 8,
                        "badge": True,
                        "pin": False,
                        "url": "/car/detail-qj73rRIf-jac-j4-1401",
                        "title": "جک، جی 4",
                        "subtitle": "1401 ",
                        "trim": "اتوماتیک",
                        "time": "لحظاتی پیش",
                        "year": "1401",
                        "mileage": "کارکرد صفر",
                        "location": "تهران / 17شهریور",
                        "specialcase": None,
                        "transmission": "اتوماتیک",
                        "fuel": "بنزینی",
                        "color": "سفید / داخل سفید",
                        "body_color": "سفید",
                        "inside_color": "سفید",
                        "body_status": "بدون رنگ",
                        "description": "⋘ نمایندگی کرمان موتور رفیعی ⋙\n\n- جک S3 (اس3) اتوماتیک\n- مدل 1401 سفید\n- صفر کیلومتر\n- دارای برگه تایید سلامت فنی و بدنه خودرو\n",
                        "authenticated": False, "body_type": "passenger_car",
                        "image_count": 3,
                        "image": "https://cdn.bama.ir/uploads/BamaImages/VehicleCarImages/73ae901f-956d-43ed-a969-f8b598afad23/CarImage10270990_638065318646860322_thumb_450_300.jpg",
                        "modified_date": "2022-12-13T12:38:37.03"},
             "images": [
                 {
                     "large": "https://cdn.bama.ir/uploads/BamaImages/VehicleCarImages/73ae901f-956d-43ed-a969-f8b598afad23/CarImage10270990_638065318646860322_thumb_900_600.jpg",
                     "small": "https://cdn.bama.ir/uploads/BamaImages/VehicleCarImages/73ae901f-956d-43ed-a969-f8b598afad23/CarImage10270990_638065318646860322_thumb_450_300.jpg",
                     "thumb": "https://cdn.bama.ir/uploads/BamaImages/VehicleCarImages/73ae901f-956d-43ed-a969-f8b598afad23/CarImage10270990_638065318646860322_thumb_240_160.jpg"},
                 {
                     "large": "https://cdn.bama.ir/uploads/BamaImages/VehicleCarImages/73ae901f-956d-43ed-a969-f8b598afad23/CarImage10270990_638065318646860414_thumb_900_600.jpg",
                     "small": "https://cdn.bama.ir/uploads/BamaImages/VehicleCarImages/73ae901f-956d-43ed-a969-f8b598afad23/CarImage10270990_638065318646860414_thumb_450_300.jpg",
                     "thumb": "https://cdn.bama.ir/uploads/BamaImages/VehicleCarImages/73ae901f-956d-43ed-a969-f8b598afad23/CarImage10270990_638065318646860414_thumb_240_160.jpg"},
                 {
                     "large": "https://cdn.bama.ir/uploads/BamaImages/VehicleCarImages/73ae901f-956d-43ed-a969-f8b598afad23/CarImage10270990_638065318646860427_thumb_900_600.jpg",
                     "small": "https://cdn.bama.ir/uploads/BamaImages/VehicleCarImages/73ae901f-956d-43ed-a969-f8b598afad23/CarImage10270990_638065318646860427_thumb_450_300.jpg",
                     "thumb": "https://cdn.bama.ir/uploads/BamaImages/VehicleCarImages/73ae901f-956d-43ed-a969-f8b598afad23/CarImage10270990_638065318646860427_thumb_240_160.jpg"}],
             "metadata": {"title_tag": "جک جی 4 فروشی ",
                          "keywords": "باما, مرجع خرید, خرید خودرو, فروش خودرو, اقساطی, ماشین, اتومبیل, ايران, جک, جی 4, 1401,  bama, buy, sell, car, brand new, second hand, used",
                          "description": "خرید خودرو جک جی 4 تولید 1401 در شهر تهران، ⋘ نمایندگی کرمان موتور رفیعی ⋙\n\n- جک S3 (اس3) اتوماتیک\n- مدل 1401 سفید\n- صفر کیلومتر\n- دارای برگه تایید سلامت فنی و بدنه خودرو\n",
                          "canonical": "https://bama.ir/car/detail-qj73rRIf-jac-j4-1401",
                          "noindex": True},
             "price": {"type": "negotiable",
                       "price": "0"},
             "ads_code": "qj73rRIf",
             "phones": {"phone": ["(021) 33523850", "(021) 33553796", "(021) 33542061", "(021) 33549425"],
                        "mobile": None}}

sheypoor_data = dic = {
    "_id": {
        "$oid": "639d5f0d6c0c67a026e2531f"
    },
    "link": "https://www.sheypoor.com/تیگو-7-پرو-بسیار-محدود-در-نمایندگی-قاسمی-418779737.html",
    "id": 418779737,
    "id_str": "418779737",
    "title": "تیگو 7 پرو بسیار محدود در نمایندگی قاسمی",
    "specs": {
        "body_type": "شاسی بلند",
        "production_year": "1401",
        "kilometers": 0,
        "model": "تیگو 7 (پرو)",
        "color": "سفید",
        "gearbox_type": "دنده‌ای",
        "body_condition": "سالم بدون خط و خش",
        "fuel_type": "بنزین"
    },
    "price_info": {
        "price": 1256000000,
        "type": "نقدی"
    },
    "text": "نمایندگی مجاز فروش و خدمات پس از فروش مدیران خودرو - کد 403 (قاسمی)\n⭐️نمایندگی برتر از نظر تیم فروش در منطقه جنوب کشور⭐\n⭐️بابیش از نیم قرن تجربه و سابقه درخشان در زمینه فروش و خدمات پس از فروش در کشور⭐️\n️جاده اصفهان نجف آباد شهر گلدشت نبش بلوار ابوذرنمایندگی کد 403 مدیران خودرو قاسمی️ \n️ پاسخگویی️️ :\n09134140986\n09134140978\n09134140943\n09134140957\n09377515079\n️تلفنهای واحد فروش: ️️\n03142235021\n03142234821\n⏰ساعات کاری 13:30-08:30 بعد از ظهر 19:30-15:30️️\n⏰روزهای جمعه وتعطیل ساعت10:00الی 13:00️️\n️جهت رفاه حال مشتریان عزیز  ثبت نام غیر حضوری هم امکانپذیرمی باشد \n️نمایندگی مجاز طرح تعویض خودروهای کارکرده مدیران خودرو با صفر کیلومتر\n️طرف قرارداد با سازمانها و ادارات دولتی با شرایط ویژه\n️شرایط فروش ویژه کارمندان دولت و بخش خصوصی\n️انتخاب رنگ خودرو بدون پرداخت اختلاف هزینه\n️تحویل خودرو با خودروبردرب منزل رایگان \n️کارواش رایگان قبل از تحویل\n<br /><br />",
    "numbers": ["09134140943"],
    "publis_date": "2022-12-17 06:15:41.275000+00:00",
    "timestamp": 1671257741,
    "location": "اصفهان، قهجاورستان",
    "user": {
        "is_auto_shop": True,
        "username": "modirankhodroghasemi403",
        "url": "https://www.sheypoor.com/shop/modirankhodroghasemi403",
        "name": "نمایندگی مدیران خودرو قاسمی کد403",
        "description": "نمایندگی فروش وخدمات پس ازفروش کد 403 مدیران خودرو<br/>با بیش از نیم قرن سابقه درخشان در زمینه فروش و خدمات پس از فروش در کشور<br/>نمایندگی برتر از نظر تیم فروش در منطقه جنوب کشور",
        "location": "اصفهان<small> . </small> جاده اصفهان نجف آباد گلدشت نبش بلوارابوذر",
        "profile_banner_url": "https://www.sheypoor.com/image/d9215e/980x0_S/shop_photos/72582/CoverImage.jpg?1662439049",
        "profile_image_url": "https://www.sheypoor.com/image/b12e8d/500x0_S/shop_photos/72582/Image.jpg?1662439049",
        "links": [],
        "working_hours": "شنبه تاپنج شنبه ساعت 8-13و15-20",
        "numbers": [
            "03142234821",
            "03142235021"
        ],
        "is_verified": False
    },
    "media": {
        "images": [
            {
                "main_url": "https://cdn.sheypoor.com/imgs/2022/12/17/418779737/666x416_Sw/418779737_aa5ea8d4819c7cc859256d5010916fdb.jpg"
            },
            {
                "main_url": "https://cdn.sheypoor.com/imgs/2022/12/17/418779737/666x416_Sw/418779737_7055b7fb756bc43e7d07ddec2f48128c.jpg"
            },
            {
                "main_url": "https://cdn.sheypoor.com/imgs/2022/12/17/418779737/666x416_Sw/418779737_301f43bda6ebb1e6a86f9c89b89712d7.jpg"
            }
        ]
    }
}
"""
