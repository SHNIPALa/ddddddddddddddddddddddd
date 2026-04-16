import asyncio
import logging
import re
import os
import json
import hashlib
import base64
from datetime import datetime
from typing import Dict, Any, Optional, List
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputFile, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import dns.resolver
import whois
import socket
import ssl
import OpenSSL
from email.utils import parseaddr

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# ВСЕ API КЛЮЧИ
NUMVERIFY_KEY = os.getenv("NUMVERIFY_KEY", "")
ABSTRACT_API_KEY = os.getenv("ABSTRACT_API_KEY", "")
VERIPHONE_KEY = os.getenv("VERIPHONE_KEY", "")
ZEROBOUNCE_KEY = os.getenv("ZEROBOUNCE_KEY", "")
VERIFALIA_KEY = os.getenv("VERIFALIA_KEY", "")
NAMEAPI_KEY = os.getenv("NAMEAPI_KEY", "")
NAMSOR_KEY = os.getenv("NAMSOR_KEY", "")
GENDERAPI_KEY = os.getenv("GENDERAPI_KEY", "")
GEOAPIFY_KEY = os.getenv("GEOAPIFY_KEY", "")
POSITIONSTACK_KEY = os.getenv("POSITIONSTACK_KEY", "")
TELEMETR_KEY = os.getenv("TELEMETR_KEY", "")
TGSTAT_KEY = os.getenv("TGSTAT_KEY", "")
TGSCAN_KEY = os.getenv("TGSCAN_KEY", "")
COMBOT_KEY = os.getenv("COMBOT_KEY", "")
IPINFO_KEY = os.getenv("IPINFO_KEY", "")
IPGEOLOCATION_KEY = os.getenv("IPGEOLOCATION_KEY", "")

storage = MemoryStorage()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

logging.basicConfig(level=logging.INFO)

class SearchStates(StatesGroup):
    choosing = State()
    phone = State()
    email = State()
    fullname = State()
    address = State()
    vk = State()
    tg = State()
    ip = State()
    password = State()
    nickname = State()
    domain = State()
    btc = State()
    eth = State()
    inn = State()
    snils = State()
    passport = State()
    vin = State()
    grz = State()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br"
}

# ============================================================
# 📱 ТЕЛЕФОН - МАКСИМАЛЬНЫЕ ДАННЫЕ (ВСЕ API + ПУБЛИЧНЫЕ ИСТОЧНИКИ)
# ============================================================

async def search_phone(phone: str) -> Dict[str, Any]:
    phone_clean = re.sub(r'[^\d+]', '', phone)
    result = {
        "номер": phone_clean,
        "формат_международный": None,
        "формат_национальный": None,
        "формат_E164": None,
        "страна": None,
        "код_страны": None,
        "регион": None,
        "город": None,
        "часовой_пояс": None,
        "оператор": None,
        "тип_линии": None,
        "валиден": False,
        "возможен": False,
        "активен": None,
        "risk_score": None,
        "fraud_score": None,
        "spam_score": None,
        "мессенджеры": [],
        "соцсети": [],
        "утечки": [],
        "отзывы": [],
        "комментарии": [],
        "связанные_имена": [],
        "связанные_адреса": [],
        "api_источники": []
    }
    
    # ===== PHONENUMBERS (локальный парсинг) =====
    try:
        pn = phonenumbers.parse(phone_clean, None)
        result["валиден"] = phonenumbers.is_valid_number(pn)
        result["возможен"] = phonenumbers.is_possible_number(pn)
        result["формат_международный"] = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        result["формат_национальный"] = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.NATIONAL)
        result["формат_E164"] = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
        result["страна"] = geocoder.description_for_number(pn, "ru")
        result["регион"] = geocoder.description_for_number(pn, "en")
        result["оператор"] = carrier.name_for_number(pn, "ru")
        tz = timezone.time_zones_for_number(pn)
        result["часовой_пояс"] = tz[0] if tz else None
    except: pass
    
    # ===== NUMVERIFY API =====
    if NUMVERIFY_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get("http://apilayer.net/api/validate", 
                    params={"access_key": NUMVERIFY_KEY, "number": phone_clean, "country_code": "", "format": 1})
                data = await r.json()
                result["api_источники"].append("NumVerify")
                if data.get("valid"):
                    result["валиден"] = True
                    if not result["страна"]: result["страна"] = data.get("country_name")
                    if not result["регион"]: result["регион"] = data.get("location")
                    if not result["оператор"]: result["оператор"] = data.get("carrier")
                    result["тип_линии"] = data.get("line_type")
        except Exception as e: result["api_источники"].append(f"NumVerify: error")
    
    # ===== ABSTRACT API =====
    if ABSTRACT_API_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get("https://phonevalidation.abstractapi.com/v1/",
                    params={"api_key": ABSTRACT_API_KEY, "phone": phone_clean})
                data = await r.json()
                result["api_источники"].append("AbstractAPI")
                if data.get("valid"):
                    result["валиден"] = True
                    if not result["страна"]: result["страна"] = data.get("country", {}).get("name")
                    if not result["оператор"]: result["оператор"] = data.get("carrier")
                    result["risk_score"] = data.get("phone_risk", {}).get("score")
        except: pass
    
    # ===== VERIPHONE API =====
    if VERIPHONE_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get("https://api.veriphone.io/v2/verify",
                    params={"key": VERIPHONE_KEY, "phone": phone_clean})
                data = await r.json()
                result["api_источники"].append("Veriphone")
                if data.get("phone_valid"):
                    result["валиден"] = True
                    if not result["страна"]: result["страна"] = data.get("country")
                    if not result["оператор"]: result["оператор"] = data.get("carrier")
                    if not result["регион"]: result["регион"] = data.get("phone_region")
        except: pass
    
    # ===== IPQUALITYSCORE (бесплатный) =====
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.get(f"https://www.ipqualityscore.com/api/json/phone/YourKey/{phone_clean}")
            data = await r.json()
            if data.get("success"):
                result["fraud_score"] = data.get("fraud_score")
                result["spam_score"] = data.get("spam_score")
                result["активен"] = data.get("active")
    except: pass
    
    # ===== ПРОВЕРКА МЕССЕНДЖЕРОВ =====
    async with aiohttp.ClientSession() as s:
        # Telegram
        try:
            r = await s.get(f"https://t.me/+{phone_clean.replace('+', '')}", headers=HEADERS, timeout=5)
            if r.status == 200: result["мессенджеры"].append({"name": "Telegram", "url": f"https://t.me/+{phone_clean.replace('+', '')}"})
        except: pass
        
        # WhatsApp проверка через публичный API
        try:
            r = await s.get(f"https://wa.me/{phone_clean.replace('+', '')}", headers=HEADERS, timeout=5)
            if r.status == 200: result["мессенджеры"].append({"name": "WhatsApp", "url": f"https://wa.me/{phone_clean.replace('+', '')}"})
        except: pass
        
        # Viber
        try:
            r = await s.get(f"https://invite.viber.com/?g2=+{phone_clean.replace('+', '')}", headers=HEADERS, timeout=5)
            if r.status == 200: result["мессенджеры"].append({"name": "Viber", "url": f"viber://chat?number=%2B{phone_clean.replace('+', '')}"})
        except: pass
    
    # ===== ПОИСК В УТЕЧКАХ =====
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.get(f"https://leakcheck.io/api/v2/query/{phone_clean}", headers={"X-API-Key": "public"})
            if r.status == 200:
                data = await r.json()
                if data.get("sources"):
                    for source in data["sources"][:5]:
                        result["утечки"].append({
                            "источник": source.get("name"),
                            "дата": source.get("date"),
                            "данные": source.get("line", "")[:100]
                        })
    except: pass
    
    # ===== КТО ЗВОНИЛ (отзывы) =====
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.get(f"https://kto-zvonil.ru/number/{phone_clean.replace('+', '')}", headers=HEADERS)
            if r.status == 200:
                t = await r.text()
                comments = re.findall(r'class="comment_text">([^<]+)<', t)
                for c in comments[:5]:
                    result["комментарии"].append(c.strip())
    except: pass
    
    return result

# ============================================================
# 📧 EMAIL - МАКСИМАЛЬНЫЕ ДАННЫЕ
# ============================================================

async def search_email(email: str) -> Dict[str, Any]:
    email = email.strip().lower()
    result = {
        "email": email,
        "локальная_часть": email.split("@")[0] if "@" in email else None,
        "домен": email.split("@")[1] if "@" in email else None,
        "формат_валиден": False,
        "валиден": False,
        "временный": False,
        "ролевой": False,
        "catch_all": False,
        "mx_записи": [],
        "spf_запись": None,
        "dmarc_запись": None,
        "dkim_найден": False,
        "whois_домена": {},
        "ssl_сертификат": {},
        "ip_адреса": [],
        "владелец": None,
        "пол": None,
        "локация": None,
        "фото": None,
        "соцсети": [],
        "утечки": [],
        "дата_создания_домена": None,
        "score": None,
        "api_источники": []
    }
    
    result["формат_валиден"] = bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
    
    if "@" not in email:
        return result
    
    domain = result["домен"]
    result["ролевой"] = any(email.startswith(p) for p in ["admin", "info", "support", "sales", "contact", "help", "noreply", "no-reply", "postmaster", "webmaster", "abuse"])
    
    # ===== DNS ПРОВЕРКИ (MX, SPF, DMARC, DKIM) =====
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        for mx in mx_records:
            result["mx_записи"].append({"приоритет": mx.preference, "сервер": str(mx.exchange)})
        result["валиден"] = len(result["mx_записи"]) > 0
    except: pass
    
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        for txt in txt_records:
            txt_str = str(txt).lower()
            if "v=spf1" in txt_str:
                result["spf_запись"] = str(txt)
            if "v=DMARC1" in txt_str:
                result["dmarc_запись"] = str(txt)
            if "dkim" in txt_str:
                result["dkim_найден"] = True
    except: pass
    
    # ===== WHOIS ДОМЕНА =====
    try:
        w = whois.whois(domain)
        result["whois_домена"] = {
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers,
            "country": w.country,
            "org": w.org
        }
        if w.creation_date:
            result["дата_создания_домена"] = str(w.creation_date)
    except: pass
    
    # ===== SSL СЕРТИФИКАТ =====
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.connect((domain, 443))
            cert = s.getpeercert()
            result["ssl_сертификат"] = {
                "issuer": dict(cert.get("issuer", [])),
                "subject": dict(cert.get("subject", [])),
                "notBefore": cert.get("notBefore"),
                "notAfter": cert.get("notAfter"),
                "serialNumber": cert.get("serialNumber")
            }
    except: pass
    
    # ===== IP АДРЕСА ДОМЕНА =====
    try:
        a_records = dns.resolver.resolve(domain, 'A')
        for a in a_records:
            result["ip_адреса"].append(str(a))
    except: pass
    
    # ===== ZEROBOUNCE API =====
    if ZEROBOUNCE_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get("https://api.zerobounce.net/v2/validate",
                    params={"email": email, "api_key": ZEROBOUNCE_KEY})
                data = await r.json()
                result["api_источники"].append("ZeroBounce")
                if data.get("status") == "valid":
                    result["валиден"] = True
                    result["временный"] = data.get("disposable") == "true"
                    result["владелец"] = f"{data.get('firstname', '')} {data.get('lastname', '')}".strip() or None
                    result["пол"] = data.get("gender")
                    result["локация"] = data.get("location")
        except: pass
    
    # ===== VERIFALIA API =====
    if VERIFALIA_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                h = {"Authorization": f"Bearer {VERIFALIA_KEY}"}
                j = await (await s.post("https://api.verifalia.com/v2.6/email-validations",
                    json={"entries": [{"inputData": email}], "quality": "high"}, headers=h)).json()
                if j.get("id"):
                    await asyncio.sleep(3)
                    r = await (await s.get(f"https://api.verifalia.com/v2.6/email-validations/{j['id']}", headers=h)).json()
                    en = r.get("entries", [{}])[0]
                    result["api_источники"].append("Verifalia")
                    result["валиден"] = result["валиден"] or en.get("status") == "Success"
                    result["временный"] = result["временный"] or en.get("disposable") == "true"
                    result["catch_all"] = en.get("catchAll") == "true"
                    result["score"] = en.get("qualityScore", 0)
        except: pass
    
    # ===== HUNTER.IO (публичный) =====
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.get(f"https://api.hunter.io/v2/email-verifier?email={email}", headers=HEADERS)
            if r.status == 200:
                data = await r.json()
                d = data.get("data", {})
                if d:
                    if not result["владелец"] and (d.get("first_name") or d.get("last_name")):
                        result["владелец"] = f"{d.get('first_name', '')} {d.get('last_name', '')}".strip()
                    if d.get("twitter"): result["соцсети"].append({"сеть": "Twitter", "url": f"https://twitter.com/{d['twitter']}"})
                    if d.get("linkedin"): result["соцсети"].append({"сеть": "LinkedIn", "url": d['linkedin']})
                    if d.get("github"): result["соцсети"].append({"сеть": "GitHub", "url": f"https://github.com/{d['github']}"})
    except: pass
    
    # ===== HIBP УТЕЧКИ =====
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", headers=HEADERS)
            if r.status == 200:
                breaches = await r.json()
                for b in breaches:
                    result["утечки"].append({
                        "название": b.get("Name"),
                        "домен": b.get("Domain"),
                        "дата": b.get("BreachDate"),
                        "данные": b.get("DataClasses", []),
                        "описание": b.get("Description"),
                        "pwn_count": b.get("PwnCount")
                    })
    except: pass
    
    # ===== GRAVATAR =====
    try:
        email_hash = hashlib.md5(email.encode()).hexdigest()
        async with aiohttp.ClientSession() as s:
            r = await s.get(f"https://www.gravatar.com/{email_hash}.json", headers=HEADERS)
            if r.status == 200:
                data = await r.json()
                entry = data.get("entry", [{}])[0]
                if not result["владелец"]:
                    result["владелец"] = entry.get("displayName") or entry.get("preferredUsername")
                if not result["локация"]:
                    result["локация"] = entry.get("currentLocation")
                result["фото"] = f"https://www.gravatar.com/avatar/{email_hash}?s=400&d=404"
                if entry.get("urls"):
                    for url in entry["urls"]:
                        result["соцсети"].append({"сеть": url.get("title"), "url": url.get("value")})
    except: pass
    
    # ===== MAILCHECK.AI (временный email) =====
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.get(f"https://api.mailcheck.ai/v1/check/{email}", headers=HEADERS)
            if r.status == 200:
                data = await r.json()
                if data.get("disposable"):
                    result["временный"] = True
    except: pass
    
    return result

# ============================================================
# 👤 ФИО - МАКСИМАЛЬНЫЕ ДАННЫЕ
# ============================================================

async def search_fullname(fio: str) -> Dict[str, Any]:
    parts = fio.strip().split()
    result = {
        "фио": fio,
        "фамилия": parts[0] if parts else None,
        "имя": parts[1] if len(parts) > 1 else None,
        "отчество": parts[2] if len(parts) > 2 else None,
        "пол": None,
        "пол_вероятность": None,
        "национальность": None,
        "национальность_вероятность": None,
        "этнос": None,
        "страна_происхождения": None,
        "возраст_примерный": None,
        "возраст_вероятность": None,
        "религия": None,
        "именины": None,
        "значение_имени": None,
        "происхождение_имени": None,
        "совместимость_имен": [],
        "известные_люди": [],
        "api_источники": []
    }
    
    name = parts[1] if len(parts) > 1 else (parts[0] if parts else "")
    surname = parts[0] if parts else ""
    
    # ===== NAMEAPI =====
    if NAMEAPI_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                d = {"inputPerson": {"name": {"nameFields": [{"stringValue": fio}]}}}
                r = await (await s.post("https://api.nameapi.org/rest/v5.3/parser/person-name-parser",
                    params={"apiKey": NAMEAPI_KEY}, json=d)).json()
                result["api_источники"].append("NameAPI")
                m = r.get("matches", [{}])[0]
                p = m.get("parsedPerson", {}).get("name", {})
                g = m.get("gender", {}).get("gender")
                result["пол"] = "Мужской" if g == "MALE" else "Женский" if g == "FEMALE" else None
                result["пол_вероятность"] = m.get("gender", {}).get("confidence")
        except: pass
    
    # ===== NAMSOR =====
    if NAMSOR_KEY and name and surname:
        try:
            async with aiohttp.ClientSession() as s:
                r = await (await s.get(f"https://v2.namsor.com/NamsorAPIv2/api2/json/genderFull/{name}/{surname}",
                    headers={"X-API-KEY": NAMSOR_KEY})).json()
                result["api_источники"].append("Namsor")
                if not result["пол"]:
                    result["пол"] = r.get("likelyGender")
                result["этнос"] = r.get("ethnicity")
                result["страна_происхождения"] = r.get("countryOrigin")
                result["религия"] = r.get("religion")
        except: pass
    
    # ===== GENDERAPI =====
    if GENDERAPI_KEY and name:
        try:
            async with aiohttp.ClientSession() as s:
                r = await (await s.get("https://gender-api.com/v2/gender",
                    params={"key": GENDERAPI_KEY, "name": name})).json()
                result["api_источники"].append("GenderAPI")
                if not result["пол"]:
                    g = r.get("gender")
                    result["пол"] = "Мужской" if g == "male" else "Женский" if g == "female" else None
                result["пол_вероятность"] = result["пол_вероятность"] or r.get("accuracy") / 100 if r.get("accuracy") else None
        except: pass
    
    # ===== AGIFY.IO (возраст) =====
    if name:
        try:
            async with aiohttp.ClientSession() as s:
                r = await (await s.get(f"https://api.agify.io?name={name}")).json()
                result["возраст_примерный"] = r.get("age")
                result["возраст_вероятность"] = r.get("count")
        except: pass
    
    # ===== NATIONALIZE.IO (национальность) =====
    if name:
        try:
            async with aiohttp.ClientSession() as s:
                r = await (await s.get(f"https://api.nationalize.io?name={name}")).json()
                countries = r.get("country", [])
                if countries:
                    country_map = {
                        "RU": "Россия", "UA": "Украина", "BY": "Беларусь", "KZ": "Казахстан",
                        "US": "США", "GB": "Великобритания", "DE": "Германия", "FR": "Франция",
                        "IT": "Италия", "ES": "Испания", "PL": "Польша", "TR": "Турция",
                        "CN": "Китай", "JP": "Япония", "IN": "Индия", "IL": "Израиль"
                    }
                    result["национальность"] = country_map.get(countries[0]["country_id"])
                    result["национальность_вероятность"] = countries[0]["probability"]
        except: pass
    
    # ===== ЗНАЧЕНИЕ ИМЕНИ =====
    if name:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get(f"https://api.nationalize.io?name={name}")
                # Используем локальную базу популярных имен
                name_meanings = {
                    "александр": {"значение": "Защитник людей", "происхождение": "Греческое"},
                    "михаил": {"значение": "Кто как Бог", "происхождение": "Еврейское"},
                    "иван": {"значение": "Бог милует", "происхождение": "Еврейское"},
                    "анна": {"значение": "Благодать", "происхождение": "Еврейское"},
                    "мария": {"значение": "Госпожа", "происхождение": "Еврейское"},
                    "елена": {"значение": "Светлая", "происхождение": "Греческое"},
                    "ольга": {"значение": "Святая", "происхождение": "Скандинавское"},
                    "татьяна": {"значение": "Устроительница", "происхождение": "Греческое"},
                    "сергей": {"значение": "Высокий", "происхождение": "Римское"},
                    "андрей": {"значение": "Мужественный", "происхождение": "Греческое"},
                    "дмитрий": {"значение": "Посвященный Деметре", "происхождение": "Греческое"},
                    "алексей": {"значение": "Защитник", "происхождение": "Греческое"},
                    "максим": {"значение": "Величайший", "происхождение": "Римское"},
                    "никита": {"значение": "Победитель", "происхождение": "Греческое"},
                    "илья": {"значение": "Сила Божия", "происхождение": "Еврейское"},
                }
                if name.lower() in name_meanings:
                    result["значение_имени"] = name_meanings[name.lower()]["значение"]
                    result["происхождение_имени"] = name_meanings[name.lower()]["происхождение"]
        except: pass
    
    return result

# ============================================================
# 🏠 АДРЕС - МАКСИМАЛЬНЫЕ ДАННЫЕ
# ============================================================

async def search_address(address: str) -> Dict[str, Any]:
    result = {
        "запрос": address,
        "найдено": False,
        "полный_адрес": None,
        "координаты": None,
        "страна": None,
        "код_страны": None,
        "регион": None,
        "город": None,
        "район": None,
        "улица": None,
        "дом": None,
        "корпус": None,
        "строение": None,
        "квартира": None,
        "почтовый_индекс": None,
        "тип_объекта": None,
        "важность": None,
        "границы": None,
        "население": None,
        "часовой_пояс": None,
        "ближайшие_объекты": [],
        "фото_места": None,
        "api_источники": []
    }
    
    # ===== GEOAPIFY =====
    if GEOAPIFY_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get("https://api.geoapify.com/v1/geocode/search",
                    params={"text": address, "apiKey": GEOAPIFY_KEY, "limit": 1, "format": "json"})
                data = await r.json()
                result["api_источники"].append("Geoapify")
                f = data.get("features", [])
                if f:
                    result["найдено"] = True
                    p = f[0].get("properties", {})
                    g = f[0].get("geometry", {})
                    result["полный_адрес"] = p.get("formatted")
                    result["координаты"] = (g.get("coordinates", [])[1], g.get("coordinates", [])[0])
                    result["страна"] = p.get("country")
                    result["код_страны"] = p.get("country_code")
                    result["регион"] = p.get("state")
                    result["город"] = p.get("city")
                    result["район"] = p.get("district") or p.get("county")
                    result["улица"] = p.get("street")
                    result["дом"] = p.get("housenumber")
                    result["почтовый_индекс"] = p.get("postcode")
                    result["тип_объекта"] = p.get("result_type")
                    result["важность"] = p.get("rank", {}).get("importance")
                    result["часовой_пояс"] = p.get("timezone", {}).get("name")
        except: pass
    
    # ===== POSITIONSTACK =====
    if POSITIONSTACK_KEY and not result["найдено"]:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get("http://api.positionstack.com/v1/forward",
                    params={"access_key": POSITIONSTACK_KEY, "query": address, "limit": 1})
                data = await r.json()
                result["api_источники"].append("PositionStack")
                d = data.get("data", [])
                if d:
                    result["найдено"] = True
                    x = d[0]
                    result["полный_адрес"] = x.get("label")
                    result["координаты"] = (x.get("latitude"), x.get("longitude"))
                    result["страна"] = x.get("country")
                    result["код_страны"] = x.get("country_code")
                    result["регион"] = x.get("region")
                    result["город"] = x.get("locality")
                    result["улица"] = x.get("street")
                    result["почтовый_индекс"] = x.get("postal_code")
        except: pass
    
    # ===== NOMINATIM (бесплатный) =====
    if not result["найдено"]:
        try:
            async with aiohttp.ClientSession() as s:
                await asyncio.sleep(1)
                r = await s.get("https://nominatim.openstreetmap.org/search",
                    params={"q": address, "format": "json", "limit": 1, "addressdetails": 1, "extratags": 1},
                    headers=HEADERS)
                data = await r.json()
                result["api_источники"].append("Nominatim")
                if data:
                    result["найдено"] = True
                    d = data[0]
                    result["полный_адрес"] = d.get("display_name")
                    result["координаты"] = (float(d["lat"]), float(d["lon"]))
                    addr = d.get("address", {})
                    result["страна"] = addr.get("country")
                    result["регион"] = addr.get("state")
                    result["город"] = addr.get("city") or addr.get("town")
                    result["улица"] = addr.get("road") or addr.get("street")
                    result["дом"] = addr.get("house_number")
                    result["почтовый_индекс"] = addr.get("postcode")
                    result["тип_объекта"] = d.get("type")
                    if "boundingbox" in d:
                        b = d["boundingbox"]
                        result["границы"] = {"юг": b[0], "север": b[1], "запад": b[2], "восток": b[3]}
                    if "extratags" in d and "population" in d["extratags"]:
                        result["население"] = d["extratags"]["population"]
        except: pass
    
    return result

# ============================================================
# ✈️ TELEGRAM - МАКСИМАЛЬНЫЕ ДАННЫЕ
# ============================================================

async def search_telegram(username: str) -> Dict[str, Any]:
    username = username.strip().replace("@", "").replace("https://t.me/", "").split("?")[0]
    result = {
        "username": username,
        "ссылка": f"https://t.me/{username}",
        "существует": False,
        "тип": None,
        "id": None,
        "имя": None,
        "фамилия": None,
        "описание": None,
        "фото": None,
        "фото_большое": None,
        "подписчики": None,
        "участники": None,
        "онлайн": None,
        "верифицирован": False,
        "скам": False,
        "реклама": False,
        "ограничения": None,
        "er": None,
        "avg_reach": None,
        "ci_index": None,
        "категория": None,
        "страна": None,
        "язык": None,
        "похожие_каналы": [],
        "api_источники": []
    }
    
    # ===== TELEMETR API =====
    if TELEMETR_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get(f"https://api.telemetr.io/v1/channel/{username}",
                    params={"api_key": TELEMETR_KEY})
                data = await r.json()
                result["api_источники"].append("Telemetr")
                if data.get("subscribers"):
                    result["существует"] = True
                    result["подписчики"] = data.get("subscribers")
                    result["er"] = data.get("er")
                    result["avg_reach"] = data.get("avg_reach")
                    result["категория"] = data.get("category")
                    result["страна"] = data.get("country")
                    result["язык"] = data.get("language")
                    result["онлайн"] = data.get("online")
        except: pass
    
    # ===== TGSTAT API =====
    if TGSTAT_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get("https://api.tgstat.ru/channels/search",
                    params={"q": username, "token": TGSTAT_KEY, "limit": 1})
                data = await r.json()
                result["api_источники"].append("TGStat")
                i = data.get("response", {}).get("items", [])
                if i:
                    result["существует"] = True
                    ch = i[0]
                    if not result["подписчики"]:
                        result["подписчики"] = ch.get("participants_count")
                    result["ci_index"] = ch.get("ci_index")
                    result["avg_reach"] = result["avg_reach"] or ch.get("daily_reach")
                    result["категория"] = result["категория"] or ch.get("category")
        except: pass
    
    # ===== TGSCAN API =====
    if TGSCAN_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get("https://api.tgscan.io/v1/search",
                    params={"q": username}, headers={"X-API-Key": TGSCAN_KEY})
                data = await r.json()
                result["api_источники"].append("TGScan")
                res = data.get("results", [])
                if res:
                    result["существует"] = True
                    ch = res[0]
                    if not result["имя"]:
                        result["имя"] = ch.get("title")
                    if not result["описание"]:
                        result["описание"] = ch.get("about")
                    result["тип"] = ch.get("type")
                    result["верифицирован"] = ch.get("verified", False)
                    if ch.get("similar_channels"):
                        result["похожие_каналы"] = ch["similar_channels"][:5]
        except: pass
    
    # ===== COMBOT API =====
    if COMBOT_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get(f"https://api.combot.io/v1/channel/{username}",
                    headers={"Authorization": f"Bearer {COMBOT_KEY}"})
                data = await r.json()
                result["api_источники"].append("Combot")
                if data.get("title"):
                    result["существует"] = True
                    if not result["имя"]:
                        result["имя"] = data.get("title")
                    if not result["описание"]:
                        result["описание"] = data.get("description")
                    result["фото"] = data.get("photo")
        except: pass
    
    # ===== ПУБЛИЧНЫЙ ПАРСИНГ =====
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.get(f"https://t.me/{username}", headers=HEADERS, timeout=10)
            if r.status == 200:
                t = await r.text()
                if "tgme_page_title" in t:
                    result["существует"] = True
                    
                    if "subscribers" in t or "members" in t:
                        result["тип"] = "Канал"
                    elif "joinchat" in t:
                        result["тип"] = "Группа"
                    else:
                        result["тип"] = "Пользователь"
                    
                    name = re.search(r'<meta property="og:title" content="([^"]+)"', t)
                    if name and not result["имя"]:
                        result["имя"] = name.group(1)
                    
                    desc = re.search(r'<meta property="og:description" content="([^"]+)"', t)
                    if desc and not result["описание"]:
                        dtext = desc.group(1)
                        if "You can contact" not in dtext:
                            result["описание"] = dtext[:500]
                            scam_keywords = ['earn', 'profit', 'signal', 'crypto', 'invest', 'заработок', 'прибыль']
                            result["скам"] = any(kw in dtext.lower() for kw in scam_keywords)
                    
                    photo = re.search(r'<meta property="og:image" content="([^"]+)"', t)
                    if photo:
                        result["фото"] = photo.group(1)
                        result["фото_большое"] = photo.group(1).replace('_40', '_400')
                    
                    id_match = re.search(r'data-peer-id="(\d+)"', t)
                    if id_match:
                        result["id"] = id_match.group(1)
                    
                    subs = re.search(r'(\d+[.,]?\d*[KkMm]?)\s+(?:subscribers|подписчик)', t)
                    if subs and not result["подписчики"]:
                        s_text = subs.group(1).replace(',', '.')
                        if 'K' in s_text.upper():
                            result["подписчики"] = int(float(s_text[:-1]) * 1000)
                        elif 'M' in s_text.upper():
                            result["подписчики"] = int(float(s_text[:-1]) * 1000000)
                        else:
                            result["подписчики"] = int(float(s_text))
    except: pass
    
    return result

# ============================================================
# 🌐 IP - МАКСИМАЛЬНЫЕ ДАННЫЕ
# ============================================================

async def search_ip(ip: str) -> Dict[str, Any]:
    result = {
        "ip": ip,
        "версия": "IPv4" if "." in ip else "IPv6",
        "страна": None,
        "код_страны": None,
        "регион": None,
        "код_региона": None,
        "город": None,
        "почтовый_индекс": None,
        "широта": None,
        "долгота": None,
        "часовой_пояс": None,
        "провайдер": None,
        "организация": None,
        "asn": None,
        "asn_org": None,
        "домен": None,
        "тип_соединения": None,
        "прокси": False,
        "vpn": False,
        "tor": False,
        "хостинг": False,
        "мобильный": False,
        "стационарный": False,
        "спутниковый": False,
        "угроза": None,
        "abuse_contact": None,
        "api_источники": []
    }
    
    # ===== IPINFO API =====
    if IPINFO_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get(f"https://ipinfo.io/{ip}", headers={"Authorization": f"Bearer {IPINFO_KEY}"})
                data = await r.json()
                result["api_источники"].append("IPInfo")
                result["город"] = data.get("city")
                result["регион"] = data.get("region")
                result["страна"] = data.get("country")
                result["почтовый_индекс"] = data.get("postal")
                result["организация"] = data.get("org")
                result["домен"] = data.get("hostname")
                if data.get("loc"):
                    lat, lon = data["loc"].split(",")
                    result["широта"] = float(lat)
                    result["долгота"] = float(lon)
                if data.get("asn"):
                    asn_info = data["asn"]
                    result["asn"] = asn_info.get("asn") if isinstance(asn_info, dict) else asn_info
                    if isinstance(asn_info, dict):
                        result["asn_org"] = asn_info.get("name")
                result["abuse_contact"] = data.get("abuse", {}).get("address") if isinstance(data.get("abuse"), dict) else None
        except: pass
    
    # ===== IPGEOLOCATION API =====
    if IPGEOLOCATION_KEY:
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get("https://api.ipgeolocation.io/ipgeo",
                    params={"apiKey": IPGEOLOCATION_KEY, "ip": ip})
                data = await r.json()
                result["api_источники"].append("IPGeolocation")
                if not result["страна"]: result["страна"] = data.get("country_name")
                if not result["код_страны"]: result["код_страны"] = data.get("country_code2")
                if not result["регион"]: result["регион"] = data.get("state_prov")
                if not result["город"]: result["город"] = data.get("city")
                if not result["почтовый_индекс"]: result["почтовый_индекс"] = data.get("zipcode")
                if not result["широта"]: result["широта"] = float(data.get("latitude", 0)) if data.get("latitude") else None
                if not result["долгота"]: result["долгота"] = float(data.get("longitude", 0)) if data.get("longitude") else None
                if not result["провайдер"]: result["провайдер"] = data.get("isp")
                if not result["организация"]: result["организация"] = data.get("organization")
                result["часовой_пояс"] = data.get("time_zone", {}).get("name")
                result["тип_соединения"] = data.get("connection_type")
        except: pass
    
    # ===== IP-API.COM =====
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.get(f"http://ip-api.com/json/{ip}?fields=66846719")
            data = await r.json()
            if data.get("status") == "success":
                result["api_источники"].append("ip-api.com")
                if not result["страна"]: result["страна"] = data.get("country")
                if not result["код_страны"]: result["код_страны"] = data.get("countryCode")
                if not result["регион"]: result["регион"] = data.get("regionName")
                if not result["город"]: result["город"] = data.get("city")
                if not result["почтовый_индекс"]: result["почтовый_индекс"] = data.get("zip")
                if not result["широта"]: result["широта"] = data.get("lat")
                if not result["долгота"]: result["долгота"] = data.get("lon")
                if not result["часовой_пояс"]: result["часовой_пояс"] = data.get("timezone")
                if not result["провайдер"]: result["провайдер"] = data.get("isp")
                if not result["организация"]: result["организация"] = data.get("org")
                if not result["asn"]: result["asn"] = data.get("as")
                result["прокси"] = data.get("proxy", False)
                result["хостинг"] = data.get("hosting", False)
                result["мобильный"] = data.get("mobile", False)
    except: pass
    
    # ===== TOR ПРОВЕРКА =====
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.get("https://check.torproject.org/exit-addresses", timeout=5)
            if r.status == 200:
                tor_list = await r.text()
                if ip in tor_list:
                    result["tor"] = True
    except: pass
    
    # ===== VPN ПРОВЕРКА =====
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.get(f"https://vpnapi.io/api/{ip}")
            if r.status == 200:
                data = await r.json()
                result["vpn"] = data.get("security", {}).get("vpn", False)
                result["прокси"] = result["прокси"] or data.get("security", {}).get("proxy", False)
                result["tor"] = result["tor"] or data.get("security", {}).get("tor", False)
    except: pass
    
    return result

# ============================================================
# 🔐 ПАРОЛЬ
# ============================================================

async def check_password(password: str) -> Dict[str, Any]:
    result = {
        "длина": len(password),
        "скомпрометирован": False,
        "количество_утечек": 0,
        "сложность": None,
        "время_взлома": None,
        "энтропия": None,
        "шаблоны": [],
        "советы": []
    }
    
    # Сложность
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    # Энтропия
    charset_size = 0
    if has_lower: charset_size += 26
    if has_upper: charset_size += 26
    if has_digit: charset_size += 10
    if has_special: charset_size += 32
    result["энтропия"] = len(password) * (charset_size.bit_length() if charset_size > 0 else 1)
    
    score = sum([has_upper, has_lower, has_digit, has_special, len(password) >= 8, len(password) >= 12, len(password) >= 16])
    
    if score <= 2:
        result["сложность"] = "Очень слабый"
        result["время_взлома"] = "Мгновенно"
    elif score <= 3:
        result["сложность"] = "Слабый"
        result["время_взлома"] = "Секунды"
    elif score <= 4:
        result["сложность"] = "Средний"
        result["время_взлома"] = "Часы"
    elif score <= 5:
        result["сложность"] = "Хороший"
        result["время_взлома"] = "Дни"
    elif score <= 6:
        result["сложность"] = "Отличный"
        result["время_взлома"] = "Месяцы"
    else:
        result["сложность"] = "Превосходный"
        result["время_взлома"] = "Годы"
    
    # Проверка шаблонов
    common_patterns = ["123", "qwerty", "password", "admin", "user", "login", "welcome"]
    for p in common_patterns:
        if p in password.lower():
            result["шаблоны"].append(p)
    
    if password.isalpha(): result["советы"].append("Добавьте цифры и спецсимволы")
    if password.islower(): result["советы"].append("Добавьте заглавные буквы")
    if len(password) < 12: result["советы"].append("Увеличьте длину до 12+ символов")
    if not has_special: result["советы"].append("Добавьте спецсимволы (!@#$%^&*)")
    
    # HIBP
    try:
        sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]
        async with aiohttp.ClientSession() as s:
            r = await s.get(f"https://api.pwnedpasswords.com/range/{prefix}", headers=HEADERS)
            if r.status == 200:
                t = await r.text()
                for line in t.splitlines():
                    if line.startswith(suffix):
                        result["скомпрометирован"] = True
                        result["количество_утечек"] = int(line.split(':')[1])
                        break
    except: pass
    
    return result

# ============================================================
# 🔍 НИКНЕЙМ - 50+ ПЛАТФОРМ
# ============================================================

async def search_nickname(username: str) -> Dict[str, Any]:
    username = username.strip().replace("@", "")
    result = {
        "username": username,
        "найдено": [],
        "не_найдено": [],
        "совпадения": 0,
        "всего_проверено": 0
    }
    
    platforms = {
        "Telegram": f"https://t.me/{username}",
        "VK": f"https://vk.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "YouTube": f"https://youtube.com/@{username}",
        "TikTok": f"https://tiktok.com/@{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Twitch": f"https://twitch.tv/{username}",
        "Pinterest": f"https://pinterest.com/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Habr": f"https://habr.com/ru/users/{username}",
        "Pikabu": f"https://pikabu.ru/@{username}",
        "Ok.ru": f"https://ok.ru/{username}",
        "LinkedIn": f"https://linkedin.com/in/{username}",
        "Behance": f"https://behance.net/{username}",
        "Dribbble": f"https://dribbble.com/{username}",
        "Flickr": f"https://flickr.com/people/{username}",
        "Patreon": f"https://patreon.com/{username}",
        "Keybase": f"https://keybase.io/{username}",
        "GitLab": f"https://gitlab.com/{username}",
        "Bitbucket": f"https://bitbucket.org/{username}",
        "CodePen": f"https://codepen.io/{username}",
        "Replit": f"https://replit.com/@{username}",
        "Dev.to": f"https://dev.to/{username}",
        "ProductHunt": f"https://producthunt.com/@{username}",
        "Mastodon": f"https://mastodon.social/@{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "Spotify": f"https://open.spotify.com/user/{username}",
        "Mixcloud": f"https://mixcloud.com/{username}",
        "About.me": f"https://about.me/{username}",
        "WordPress": f"https://{username}.wordpress.com",
        "Blogger": f"https://{username}.blogspot.com",
        "LiveJournal": f"https://{username}.livejournal.com",
        "AngelList": f"https://angel.co/{username}",
        "HackerNews": f"https://news.ycombinator.com/user?id={username}",
        "Gravatar": f"https://gravatar.com/{username}",
        "Disqus": f"https://disqus.com/by/{username}",
        "Imgur": f"https://imgur.com/user/{username}",
        "DeviantArt": f"https://deviantart.com/{username}",
        "500px": f"https://500px.com/{username}",
        "Last.fm": f"https://last.fm/user/{username}",
        "MyAnimeList": f"https://myanimelist.net/profile/{username}",
        "Roblox": f"https://roblox.com/user.aspx?username={username}",
        "Minecraft": f"https://namemc.com/profile/{username}",
        "FortniteTracker": f"https://fortnitetracker.com/profile/all/{username}",
        "Chess.com": f"https://chess.com/member/{username}",
        "Kaggle": f"https://kaggle.com/{username}",
        "SlideShare": f"https://slideshare.net/{username}",
        "Scribd": f"https://scribd.com/{username}",
        "Issuu": f"https://issuu.com/{username}",
        "Wattpad": f"https://wattpad.com/user/{username}",
        "Goodreads": f"https://goodreads.com/{username}",
        "Letterboxd": f"https://letterboxd.com/{username}",
        "Trakt": f"https://trakt.tv/users/{username}",
        "Foursquare": f"https://foursquare.com/{username}",
        "TripAdvisor": f"https://tripadvisor.com/members/{username}",
        "Yelp": f"https://yelp.com/user_details?userid={username}",
        "Etsy": f"https://etsy.com/people/{username}",
        "eBay": f"https://ebay.com/usr/{username}",
        "Amazon": f"https://amazon.com/gp/profile/{username}",
        "PayPal": f"https://paypal.me/{username}",
        "Venmo": f"https://venmo.com/{username}",
        "CashApp": f"https://cash.app/${username}",
        "Ko-fi": f"https://ko-fi.com/{username}",
        "BuyMeACoffee": f"https://buymeacoffee.com/{username}"
    }
    
    async with aiohttp.ClientSession() as s:
        tasks = []
        for name, url in platforms.items():
            tasks.append(check_platform(s, name, url))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for r in results:
            if isinstance(r, dict):
                result["всего_проверено"] += 1
                if r.get("найден"):
                    result["найдено"].append(r)
                    result["совпадения"] += 1
                else:
                    result["не_найдено"].append(r["платформа"])
    
    return result

async def check_platform(session, name, url):
    try:
        r = await session.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
        if r.status == 200:
            return {"платформа": name, "ссылка": url, "найден": True}
        return {"платформа": name, "найден": False}
    except:
        return {"платформа": name, "найден": False}

# ============================================================
# 📘 VK - ПУБЛИЧНЫЙ ПОИСК
# ============================================================

async def search_vk(user_input: str) -> Dict[str, Any]:
    user_input = user_input.strip().replace("https://vk.com/", "").replace("vk.com/", "").replace("@", "")
    result = {
        "запрос": user_input,
        "найден": False,
        "id": None,
        "имя": None,
        "фамилия": None,
        "девичья": None,
        "статус": None,
        "день_рождения": None,
        "возраст": None,
        "город": None,
        "страна": None,
        "телефон": None,
        "сайт": None,
        "образование": [],
        "работа": [],
        "друзья": None,
        "подписчики": None,
        "фотографии": None,
        "видео": None,
        "аудио": None,
        "аватар": None,
        "обложка": None,
        "верифицирован": False,
        "онлайн": False,
        "устройство": None,
        "последний_визит": None,
        "группы": []
    }
    
    try:
        async with aiohttp.ClientSession() as s:
            url = f"https://vk.com/id{user_input}" if user_input.isdigit() else f"https://vk.com/{user_input}"
            r = await s.get(url, headers=HEADERS, timeout=10)
            if r.status == 200:
                t = await r.text()
                if "Page not found" not in t and "Страница не найдена" not in t:
                    result["найден"] = True
                    
                    title = re.search(r'<title>([^<]+)</title>', t)
                    if title:
                        full = title.group(1).replace(" | ВКонтакте", "").strip()
                        parts = full.split()
                        if parts:
                            result["имя"] = parts[0]
                            if len(parts) > 1:
                                result["фамилия"] = parts[-1]
                    
                    idm = re.search(r'data-owner-id="(\d+)"', t)
                    if idm: result["id"] = idm.group(1)
                    
                    maiden = re.search(r'девичья фамилия.*?>([^<]+)<', t, re.I)
                    if maiden: result["девичья"] = maiden.group(1).strip()
                    
                    status = re.search(r'class="profile_status">([^<]+)<', t)
                    if status: result["статус"] = status.group(1).strip()
                    
                    bdate = re.search(r'День рождения:.*?>([^<]+)<', t)
                    if bdate:
                        bd = bdate.group(1).strip()
                        result["день_рождения"] = bd
                        year = re.search(r'(\d{4})', bd)
                        if year: result["возраст"] = datetime.now().year - int(year.group(1))
                    
                    city = re.search(r'Город:.*?>([^<]+)<', t)
                    if city: result["город"] = city.group(1).strip()
                    
                    country = re.search(r'Страна:.*?>([^<]+)<', t)
                    if country: result["страна"] = country.group(1).strip()
                    
                    phone = re.search(r'Моб\. телефон:.*?>([^<]+)<', t)
                    if phone: result["телефон"] = phone.group(1).strip()
                    
                    site = re.search(r'Веб-сайт:.*?href="([^"]+)"', t)
                    if site: result["сайт"] = site.group(1)
                    
                    edu = re.findall(r'class="profile_edu_place">([^<]+)<', t)
                    result["образование"] = [e.strip() for e in edu[:5]]
                    
                    work = re.findall(r'class="profile_job_place">([^<]+)<', t)
                    result["работа"] = [w.strip() for w in work[:5]]
                    
                    friends = re.search(r'(\d+)\s+друзей', t)
                    if friends: result["друзья"] = int(friends.group(1))
                    
                    followers = re.search(r'(\d+)\s+подписчик', t)
                    if followers: result["подписчики"] = int(followers.group(1))
                    
                    photos = re.search(r'(\d+)\s+фотографи', t)
                    if photos: result["фотографии"] = int(photos.group(1))
                    
                    videos = re.search(r'(\d+)\s+видеозапис', t)
                    if videos: result["видео"] = int(videos.group(1))
                    
                    audios = re.search(r'(\d+)\s+аудиозапис', t)
                    if audios: result["аудио"] = int(audios.group(1))
                    
                    ava = re.search(r'<meta property="og:image" content="([^"]+)"', t)
                    if ava: result["аватар"] = ava.group(1)
                    
                    cover = re.search(r'class="page_cover_img"[^>]+style="background-image:url\(([^)]+)\)', t)
                    if cover: result["обложка"] = cover.group(1)
                    
                    result["верифицирован"] = 'page_verified' in t
                    result["онлайн"] = 'profile_online_lv' in t
                    
                    device = re.search(r'class="profile_online_lv">([^<]+)<', t)
                    if device: result["устройство"] = device.group(1).strip()
                    
                    last = re.search(r'Заходила?\s+(\d+\s+\w+\s+\d+\s+в\s+[\d:]+)', t)
                    if last: result["последний_визит"] = last.group(1)
                    
                    groups = re.findall(r'href="/([^"]+)"[^>]*>([^<]+)</a>\s*</div>\s*<div[^>]*>\s*(\d+)\s*подпис', t)
                    for g in groups[:10]:
                        result["группы"].append({"ссылка": g[0], "название": g[1].strip(), "подписчики": g[2] if len(g) > 2 else None})
    except: pass
    
    return result

# ============================================================
# МЕНЮ И ХЕНДЛЕРЫ
# ============================================================

def menu():
    b = InlineKeyboardBuilder()
    buttons = [
        ("📱 Телефон", "phone"), ("📧 Email", "email"), ("👤 ФИО", "fullname"),
        ("🏠 Адрес", "address"), ("📘 VK", "vk"), ("✈️ Telegram", "tg"),
        ("🌐 IP", "ip"), ("🔐 Пароль", "password"), ("🔍 Никнейм", "nickname")
    ]
    for t, d in buttons:
        b.button(text=t, callback_data=d)
    b.adjust(2)
    return b.as_markup()

@dp.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>🔍 VICTIM OSINT</b>\n\n"
        "✅ ВСЕ API ПОДКЛЮЧЕНЫ\n"
        "✅ МАКСИМАЛЬНЫЙ СБОР ДАННЫХ\n\n"
        "NumVerify, AbstractAPI, Veriphone\n"
        "ZeroBounce, Verifalia\n"
        "NameAPI, Namsor, GenderAPI\n"
        "Geoapify, PositionStack\n"
        "Telemetr, TGStat, TGScan, Combot\n"
        "IPInfo, IPGeolocation\n\n"
        "Выберите сегмент:",
        reply_markup=menu()
    )
    await state.set_state(SearchStates.choosing)

@dp.callback_query(F.data == "back")
async def back_cb(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchStates.choosing)
    await callback.message.edit_text("<b>🔍 VICTIM OSINT</b>\n\nВсе API подключены.", reply_markup=menu())
    await callback.answer()

@dp.callback_query(SearchStates.choosing)
async def choice_cb(callback: CallbackQuery, state: FSMContext):
    d = callback.data
    prompts = {
        "phone": (SearchStates.phone, "📱 <b>Введите номер телефона</b>"),
        "email": (SearchStates.email, "📧 <b>Введите Email</b>"),
        "fullname": (SearchStates.fullname, "👤 <b>Введите ФИО</b>"),
        "address": (SearchStates.address, "🏠 <b>Введите адрес</b>"),
        "vk": (SearchStates.vk, "📘 <b>Введите VK ID или ник</b>"),
        "tg": (SearchStates.tg, "✈️ <b>Введите Telegram username</b>"),
        "ip": (SearchStates.ip, "🌐 <b>Введите IP адрес</b>"),
        "password": (SearchStates.password, "🔐 <b>Введите пароль</b>"),
        "nickname": (SearchStates.nickname, "🔍 <b>Введите никнейм</b>")
    }
    if d in prompts:
        ns, pt = prompts[d]
        await state.set_state(ns)
        await callback.message.edit_text(pt, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]))
    await callback.answer()

def format_phone_result(r):
    t = f"<b>📱 {r['номер']}</b>\n\n"
    if r.get("формат_международный"): t += f"🌍 {r['формат_международный']}\n"
    if r.get("страна"): t += f"🇷🇺 Страна: {r['страна']}\n"
    if r.get("регион"): t += f"📍 Регион: {r['регион']}\n"
    if r.get("оператор"): t += f"📡 Оператор: {r['оператор']}\n"
    if r.get("часовой_пояс"): t += f"🕐 Часовой пояс: {r['часовой_пояс']}\n"
    if r.get("тип_линии"): t += f"📞 Тип: {r['тип_линии']}\n"
    t += f"✅ Валиден: {'Да' if r['валиден'] else 'Нет'}\n"
    if r.get("risk_score"): t += f"⚠️ Risk: {r['risk_score']}/100\n"
    if r.get("мессенджеры"):
        t += "\n<b>💬 Мессенджеры:</b>\n"
        for m in r["мессенджеры"]:
            t += f"• {m['name']}\n"
    if r.get("комментарии"):
        t += "\n<b>📝 Отзывы:</b>\n"
        for c in r["комментарии"][:3]:
            t += f"• {c[:100]}...\n"
    if r.get("api_источники"):
        t += f"\n📡 API: {', '.join(r['api_источники'])}"
    return t

def format_email_result(r):
    t = f"<b>📧 {r['email']}</b>\n\n"
    t += f"✅ Формат: {'OK' if r['формат_валиден'] else 'Ошибка'}\n"
    if r.get("домен"): t += f"🌐 Домен: {r['домен']}\n"
    t += f"📧 Валиден: {'Да' if r['валиден'] else 'Нет'}\n"
    t += f"⚠️ Временный: {'Да' if r['временный'] else 'Нет'}\n"
    if r.get("владелец"): t += f"👤 Владелец: {r['владелец']}\n"
    if r.get("пол"): t += f"⚥ Пол: {r['пол']}\n"
    if r.get("локация"): t += f"📍 Локация: {r['локация']}\n"
    if r.get("mx_записи"):
        t += "\n<b>📡 MX записи:</b>\n"
        for mx in r["mx_записи"][:3]:
            t += f"• {mx['сервер']} (приоритет: {mx['приоритет']})\n"
    if r.get("whois_домена") and r["whois_домена"].get("creation_date"):
        t += f"\n📅 Домен создан: {r['whois_домена']['creation_date']}\n"
    if r.get("утечки"):
        t += f"\n<b>🔴 Утечки ({len(r['утечки'])}):</b>\n"
        for u in r["утечки"][:5]:
            t += f"• {u['название']} ({u.get('дата', 'N/A')})\n"
    if r.get("api_источники"):
        t += f"\n📡 API: {', '.join(r['api_источники'])}"
    return t

def format_fullname_result(r):
    t = f"<b>👤 {r['фио']}</b>\n\n"
    if r.get("пол"): t += f"⚥ Пол: {r['пол']}"
    if r.get("пол_вероятность"): t += f" ({r['пол_вероятность']*100:.0f}%)\n"
    else: t += "\n"
    if r.get("национальность"): t += f"🌍 Национальность: {r['национальность']}\n"
    if r.get("страна_происхождения"): t += f"🇷🇺 Страна: {r['страна_происхождения']}\n"
    if r.get("этнос"): t += f"👥 Этнос: {r['этнос']}\n"
    if r.get("возраст_примерный"): t += f"📅 Возраст: ~{r['возраст_примерный']} лет\n"
    if r.get("религия"): t += f"🕊 Религия: {r['религия']}\n"
    if r.get("значение_имени"): t += f"📖 Значение имени: {r['значение_имени']}\n"
    if r.get("api_источники"):
        t += f"\n📡 API: {', '.join(r['api_источники'])}"
    return t

def format_address_result(r):
    t = f"<b>🏠 Адрес</b>\n\n"
    if r.get("найдено"):
        t += "✅ <b>Найден</b>\n"
        if r.get("полный_адрес"): t += f"📍 {r['полный_адрес'][:200]}...\n\n"
        if r.get("страна"): t += f"🌍 Страна: {r['страна']}\n"
        if r.get("регион"): t += f"🏛 Регион: {r['регион']}\n"
        if r.get("город"): t += f"🏙 Город: {r['город']}\n"
        if r.get("улица"): t += f"🛣 Улица: {r['улица']}\n"
        if r.get("дом"): t += f"🏠 Дом: {r['дом']}\n"
        if r.get("почтовый_индекс"): t += f"📮 Индекс: {r['почтовый_индекс']}\n"
        if r.get("координаты"):
            lat, lon = r["координаты"]
            t += f"🗺 Координаты: {lat:.6f}, {lon:.6f}\n"
    else:
        t += "❌ <b>Адрес не найден</b>\n"
    if r.get("api_источники"):
        t += f"\n📡 API: {', '.join(r['api_источники'])}"
    return t

def format_telegram_result(r):
    t = f"<b>✈️ @{r['username']}</b>\n\n"
    if r.get("существует"):
        t += "✅ <b>Существует</b>\n"
        if r.get("тип"): t += f"📌 Тип: {r['тип']}\n"
        if r.get("имя"): t += f"👤 Имя: {r['имя']}\n"
        if r.get("id"): t += f"🆔 ID: {r['id']}\n"
        if r.get("описание"): t += f"📝 Описание: {r['описание'][:200]}...\n"
        if r.get("подписчики"): t += f"👥 Подписчиков: {r['подписчики']:,}\n".replace(',', ' ')
        if r.get("er"): t += f"📊 ER: {r['er']:.2f}%\n"
        if r.get("avg_reach"): t += f"📈 Охват: {r['avg_reach']:,}\n".replace(',', ' ')
        if r.get("ci_index"): t += f"📊 CI: {r['ci_index']:.2f}\n"
        if r.get("категория"): t += f"📂 Категория: {r['категория']}\n"
        if r.get("страна"): t += f"🌍 Страна: {r['страна']}\n"
        t += f"✅ Верифицирован: {'Да' if r['верифицирован'] else 'Нет'}\n"
        t += f"⚠️ Скам: {'Да' if r['скам'] else 'Нет'}\n"
    else:
        t += "❌ <b>Не найден</b>\n"
    if r.get("api_источники"):
        t += f"\n📡 API: {', '.join(r['api_источники'])}"
    return t

def format_ip_result(r):
    t = f"<b>🌐 {r['ip']}</b>\n\n"
    if r.get("страна"): t += f"🌍 Страна: {r['страна']} ({r.get('код_страны', '')})\n"
    if r.get("регион"): t += f"📍 Регион: {r['регион']}\n"
    if r.get("город"): t += f"🏙 Город: {r['город']}\n"
    if r.get("почтовый_индекс"): t += f"📮 Индекс: {r['почтовый_индекс']}\n"
    if r.get("провайдер"): t += f"📡 Провайдер: {r['провайдер']}\n"
    if r.get("организация"): t += f"🏢 Организация: {r['организация']}\n"
    if r.get("asn"): t += f"🔢 ASN: {r['asn']}\n"
    if r.get("часовой_пояс"): t += f"🕐 Часовой пояс: {r['часовой_пояс']}\n"
    t += f"\n⚠️ Прокси: {'Да' if r['прокси'] else 'Нет'}\n"
    t += f"🔒 VPN: {'Да' if r['vpn'] else 'Нет'}\n"
    t += f"🌐 TOR: {'Да' if r['tor'] else 'Нет'}\n"
    t += f"🖥 Хостинг: {'Да' if r['хостинг'] else 'Нет'}\n"
    if r.get("api_источники"):
        t += f"\n📡 API: {', '.join(r['api_источники'])}"
    return t

def format_password_result(r):
    t = "<b>🔐 Анализ пароля</b>\n\n"
    t += f"📏 Длина: {r['длина']} символов\n"
    t += f"📊 Сложность: {r['сложность']}\n"
    t += f"⏱ Время взлома: {r['время_взлома']}\n"
    if r.get("энтропия"): t += f"🔢 Энтропия: {r['энтропия']} бит\n"
    if r.get("скомпрометирован"):
        t += f"\n🔴 <b>СКОМПРОМЕТИРОВАН!</b>\n"
        t += f"📊 Найден в утечках: {r['количество_утечек']:,} раз\n".replace(',', ' ')
    else:
        t += "\n✅ Не найден в утечках\n"
    if r.get("советы"):
        t += f"\n<b>💡 Рекомендации:</b>\n"
        for tip in r["советы"]:
            t += f"• {tip}\n"
    return t

def format_nickname_result(r):
    t = f"<b>🔍 @{r['username']}</b>\n\n"
    t += f"📊 Найдено: {r['совпадения']} из {r['всего_проверено']}\n\n"
    if r.get("найдено"):
        t += "<b>✅ Найденные профили:</b>\n"
        for p in r["найдено"]:
            t += f"• <a href='{p['ссылка']}'>{p['платформа']}</a>\n"
    return t

def format_vk_result(r):
    t = f"<b>📘 VK: {r['запрос']}</b>\n\n"
    if r.get("найден"):
        t += "✅ <b>Профиль найден</b>\n"
        if r.get("id"): t += f"🆔 ID: {r['id']}\n"
        if r.get("имя"): t += f"👤 Имя: {r['имя']} {r.get('фамилия', '')}\n"
        if r.get("девичья"): t += f"👰 Девичья: {r['девичья']}\n"
        if r.get("статус"): t += f"💬 Статус: {r['статус']}\n"
        if r.get("день_рождения"): t += f"🎂 ДР: {r['день_рождения']}"
        if r.get("возраст"): t += f" ({r['возраст']} лет)\n"
        else: t += "\n"
        if r.get("город"): t += f"🏙 Город: {r['город']}\n"
        if r.get("страна"): t += f"🌍 Страна: {r['страна']}\n"
        if r.get("телефон"): t += f"📱 Телефон: {r['телефон']}\n"
        if r.get("друзья"): t += f"👥 Друзей: {r['друзья']}\n"
        if r.get("подписчики"): t += f"📊 Подписчиков: {r['подписчики']}\n"
        t += f"🟢 Онлайн: {'Да' if r['онлайн'] else 'Нет'}\n"
    else:
        t += "❌ <b>Профиль не найден</b>\n"
    return t

@dp.message(SearchStates.phone)
async def phone_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Сбор данных...")
    r = await search_phone(message.text.strip())
    await w.delete()
    await message.answer(format_phone_result(r), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑 Удалить", callback_data="del"), InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]), disable_web_page_preview=True)
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.email)
async def email_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Сбор данных...")
    r = await search_email(message.text.strip())
    await w.delete()
    if r.get("фото"):
        try: await message.answer_photo(r["фото"], caption="📸 Gravatar")
        except: pass
    await message.answer(format_email_result(r), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑 Удалить", callback_data="del"), InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]), disable_web_page_preview=True)
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.fullname)
async def fullname_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Анализ ФИО...")
    r = await search_fullname(message.text.strip())
    await w.delete()
    await message.answer(format_fullname_result(r), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑 Удалить", callback_data="del"), InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]))
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.address)
async def address_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Геокодирование...")
    r = await search_address(message.text.strip())
    await w.delete()
    if r.get("координаты"):
        lat, lon = r["координаты"]
        await message.answer_location(lat, lon)
    await message.answer(format_address_result(r), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑 Удалить", callback_data="del"), InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]), disable_web_page_preview=True)
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.vk)
async def vk_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Поиск VK...")
    r = await search_vk(message.text.strip())
    await w.delete()
    if r.get("аватар"):
        try: await message.answer_photo(r["аватар"], caption="📸 Аватар")
        except: pass
    await message.answer(format_vk_result(r), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑 Удалить", callback_data="del"), InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]), disable_web_page_preview=True)
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.tg)
async def tg_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Сбор данных Telegram...")
    r = await search_telegram(message.text.strip())
    await w.delete()
    if r.get("фото_большое"):
        try: await message.answer_photo(r["фото_большое"], caption="📸 Фото профиля")
        except: pass
    elif r.get("фото"):
        try: await message.answer_photo(r["фото"])
        except: pass
    await message.answer(format_telegram_result(r), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑 Удалить", callback_data="del"), InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]), disable_web_page_preview=True)
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.ip)
async def ip_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Сбор данных IP...")
    r = await search_ip(message.text.strip())
    await w.delete()
    if r.get("широта") and r.get("долгота"):
        await message.answer_location(r["широта"], r["долгота"])
    await message.answer(format_ip_result(r), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑 Удалить", callback_data="del"), InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]), disable_web_page_preview=True)
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.password)
async def password_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Проверка пароля...")
    r = await check_password(message.text.strip())
    try: await message.delete()
    except: pass
    await w.delete()
    msg = await message.answer(format_password_result(r), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑 Удалить", callback_data="del"), InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]))
    asyncio.create_task(auto_delete(msg, 60))
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.nickname)
async def nickname_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Поиск по 70+ платформам...")
    r = await search_nickname(message.text.strip())
    await w.delete()
    await message.answer(format_nickname_result(r), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑 Удалить", callback_data="del"), InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]), disable_web_page_preview=True)
    await state.set_state(SearchStates.choosing)

async def auto_delete(msg, d):
    await asyncio.sleep(d)
    try: await msg.delete()
    except: pass

@dp.callback_query(F.data == "del")
async def delete_cb(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
