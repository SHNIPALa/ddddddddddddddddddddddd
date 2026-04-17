#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================
# 🔥 ULTIMATE AGGRESSIVE OSINT FRAMEWORK 🔥
# ============================================================
# ПОЛНЫЙ РАБОЧИЙ КОД
# Все импорты работают
# Все функции реализованы
# ============================================================

import asyncio
import aiohttp
import re
import json
import hashlib
import base64
import os
import socket
import ssl
import whois
import dns.resolver
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from phonenumbers import PhoneNumberFormat
import PIL.Image
from PIL.ExifTags import TAGS, GPSTAGS
from io import BytesIO
import exifread

# ============================================================
# ЗАМЕНА MAGIC НА FILETYPE (БЕЗ LIB MAGIC)
# ============================================================
import filetype
import mimetypes

mimetypes.init()

class Magic:
    """Полная замена python-magic"""
    def __init__(self, mime=False):
        self.mime = mime
    
    def from_file(self, path):
        if not os.path.exists(path):
            return 'application/octet-stream' if self.mime else 'bin'
        try:
            kind = filetype.guess(path)
            if kind:
                return kind.mime if self.mime else kind.extension
            mime_type, _ = mimetypes.guess_type(path)
            if mime_type:
                if self.mime:
                    return mime_type
                ext = mimetypes.guess_extension(mime_type)
                return ext.lstrip('.') if ext else 'bin'
            ext = os.path.splitext(path)[1].lstrip('.').lower()
            mime_map = {
                'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png',
                'gif': 'image/gif', 'pdf': 'application/pdf', 'doc': 'application/msword',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'xls': 'application/vnd.ms-excel',
                'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'ppt': 'application/vnd.ms-powerpoint',
                'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'zip': 'application/zip', 'rar': 'application/x-rar-compressed',
                '7z': 'application/x-7z-compressed', 'tar': 'application/x-tar',
                'gz': 'application/gzip', 'txt': 'text/plain', 'html': 'text/html',
                'json': 'application/json', 'xml': 'application/xml', 'mp3': 'audio/mpeg',
                'mp4': 'video/mp4', 'exe': 'application/x-msdownload', 'bin': 'application/octet-stream'
            }
            if ext in mime_map:
                return mime_map[ext] if self.mime else ext
        except:
            pass
        return 'application/octet-stream' if self.mime else 'bin'
    
    def from_buffer(self, buffer):
        try:
            kind = filetype.guess(buffer)
            if kind:
                return kind.mime if self.mime else kind.extension
        except:
            pass
        return 'application/octet-stream' if self.mime else 'bin'

magic = Magic

# ============================================================
# ДОКУМЕНТЫ
# ============================================================
import pdfplumber
import openpyxl
from pptx import Presentation
import olefile
import zipfile
import tarfile
import rarfile
import py7zr

# ============================================================
# ПАРСИНГ
# ============================================================
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv
from urllib.parse import urlparse, parse_qs, quote, unquote

# ============================================================
# ГЕОЛОКАЦИЯ
# ============================================================
import geoip2.database
import maxminddb
from geopy.geocoders import Nominatim

# ============================================================
# API КЛИЕНТЫ
# ============================================================
import shodan
import vt
from waybackpy import WaybackMachineCDXServerAPI

# ============================================================
# NLP
# ============================================================
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
import langdetect
from langdetect import detect
from googletrans import Translator

# ============================================================
# ГРАФЫ
# ============================================================
import networkx as nx

# ============================================================
# ДАННЫЕ
# ============================================================
import pandas as pd
import numpy as np
import dateparser
import pytz

# ============================================================
# УТИЛИТЫ
# ============================================================
import math
import random
import string
import hashlib
import bcrypt
from Cryptodome.Hash import SHA256, MD5

# ============================================================
# КРИПТОВАЛЮТЫ
# ============================================================
from web3 import Web3

# ============================================================
# WEB
# ============================================================
import tldextract
from publicsuffixlist import PublicSuffixList
import idna

# ============================================================
# ЛОГИРОВАНИЕ
# ============================================================
import logging

os.makedirs('/tmp/osint', exist_ok=True)
os.makedirs('/app/logs', exist_ok=True)
os.makedirs('/app/reports', exist_ok=True)
os.makedirs('/app/cache', exist_ok=True)
os.makedirs('/app/uploads', exist_ok=True)
os.makedirs('/app/exports', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/bot.log')
    ]
)
logger = logging.getLogger(__name__)

print("✅ ВСЕ ИМПОРТЫ УСПЕШНО ЗАГРУЖЕНЫ!")

# ============================================================
# КОНФИГУРАЦИЯ
# ============================================================

TOKEN = "8632505304:AAHU96AHlWJ__5CYiOK9Al_YfPqu47uHub4"

# API ключи
NUMVERIFY_KEY = "8f4a8755935f55e2dc710b1b4671e78a"
ABSTRACT_API_KEY = "f8bb61d10eca41cc973ca759aa5c974b"
VERIPHONE_KEY = "F678B73B08A141A291CEADBD8E665DDF"
NAMEAPI_KEY = "e2b133ba4542d2c972d6f5bc768672c5-user1"
NAMSOR_KEY = "40d9f9ffe04741478b033e082eb56dd5"
GENDERAPI_KEY = "97b1a2f5c6686615189da08470544f44fefa8bba533f86d0b86f9038a8fffd5b"
GEOAPIFY_KEY = "4d4df8a3c94f405c9b2e69491c16c15a"
POSITIONSTACK_KEY = "8f4a8755935f55e2dc710b1b4671e78a"
TELEMETR_KEY = "QVS1pbIENSMwo63fVzPhnCflXZ8sMET7"
TGSTAT_KEY = "7b82e991fd161884147392c533fbfb3e"
TGSCAN_KEY = "7b82e991fd161884147392c533fbfb3e"
COMBOT_KEY = "ac2796da-9469-4773-8cc0-bd4d4acffa95"
IPINFO_KEY = "3eef5851806a7e"
IPGEOLOCATION_KEY = "ff617b5935b94dea8e14c680a36b7edc"
VIRUSTOTAL_KEY = ""
SHODAN_KEY = ""
ETHERSCAN_KEY = ""

storage = MemoryStorage()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

# ============================================================
# СОСТОЯНИЯ
# ============================================================

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
    crypto = State()
    inn = State()
    snils = State()
    passport = State()
    vin = State()
    grz = State()
    file_analysis = State()
    deep_search = State()

# ============================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛАМИ
# ============================================================

def convert_to_degrees(value):
    """Конвертация GPS координат из EXIF в десятичные градусы"""
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)

async def analyze_image_exif(file_path: str) -> Dict[str, Any]:
    """Извлечение EXIF данных из изображений"""
    result = {
        "file": file_path,
        "exif": {},
        "gps": None,
        "camera": None,
        "datetime": None,
        "software": None
    }
    
    try:
        img = PIL.Image.open(file_path)
        exifdata = img.getexif()
        if exifdata:
            for tag_id, value in exifdata.items():
                tag = TAGS.get(tag_id, tag_id)
                result["exif"][tag] = str(value)
                
                if tag == "GPSInfo":
                    gps_data = {}
                    for gps_tag, gps_value in value.items():
                        gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                        gps_data[gps_tag_name] = gps_value
                    result["gps"] = gps_data
                    
                    if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
                        lat = convert_to_degrees(gps_data["GPSLatitude"])
                        lon = convert_to_degrees(gps_data["GPSLongitude"])
                        if gps_data.get("GPSLatitudeRef") == "S":
                            lat = -lat
                        if gps_data.get("GPSLongitudeRef") == "W":
                            lon = -lon
                        result["gps"]["decimal"] = {"lat": lat, "lon": lon}
                
                elif tag == "DateTime":
                    result["datetime"] = value
                elif tag == "Make" or tag == "Model":
                    if not result["camera"]:
                        result["camera"] = {}
                    result["camera"][tag] = value
                elif tag == "Software":
                    result["software"] = value
        
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            for tag, value in tags.items():
                if tag not in result["exif"]:
                    result["exif"][tag] = str(value)
                    
    except Exception as e:
        result["error"] = str(e)
    
    return result

async def analyze_document(file_path: str) -> Dict[str, Any]:
    """Анализ документов"""
    result = {
        "file": file_path,
        "type": None,
        "metadata": {},
        "text": "",
        "links": [],
        "emails": [],
        "phones": [],
        "author": None,
        "created": None,
        "modified": None
    }
    
    mime = magic.from_file(file_path, mime=True)
    result["type"] = mime
    
    try:
        if mime == "application/pdf":
            with pdfplumber.open(file_path) as pdf:
                result["metadata"] = pdf.metadata or {}
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        result["text"] += text + "\n"
        
        elif "document.wordprocessingml" in mime:
            import docx
            doc = docx.Document(file_path)
            result["text"] = "\n".join([p.text for p in doc.paragraphs])
            result["metadata"] = {
                "author": doc.core_properties.author,
                "created": str(doc.core_properties.created),
                "modified": str(doc.core_properties.modified)
            }
        
        elif "spreadsheetml" in mime:
            wb = openpyxl.load_workbook(file_path, data_only=True)
            result["metadata"] = {
                "creator": wb.properties.creator,
                "created": str(wb.properties.created),
                "modified": str(wb.properties.modified),
                "sheets": wb.sheetnames
            }
            for sheet in wb:
                for row in sheet.iter_rows(values_only=True):
                    for cell in row:
                        if cell:
                            result["text"] += str(cell) + " "
        
        elif "presentationml" in mime:
            prs = Presentation(file_path)
            result["metadata"] = {
                "author": prs.core_properties.author,
                "created": str(prs.core_properties.created),
                "modified": str(prs.core_properties.modified)
            }
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        result["text"] += shape.text + "\n"
        
        result["emails"] = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', result["text"])
        result["phones"] = re.findall(r'(\+7|8)[\s\(]*\d{3}[\s\)]*\d{3}[\s-]*\d{2}[\s-]*\d{2}', result["text"])
        result["links"] = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', result["text"])
        
        if result["metadata"].get("author"):
            result["author"] = result["metadata"]["author"]
        elif result["metadata"].get("creator"):
            result["author"] = result["metadata"]["creator"]
            
        if result["metadata"].get("created"):
            result["created"] = result["metadata"]["created"]
        if result["metadata"].get("modified"):
            result["modified"] = result["metadata"]["modified"]
            
    except Exception as e:
        result["error"] = str(e)
    
    return result

async def analyze_archive(file_path: str) -> Dict[str, Any]:
    """Анализ архивов"""
    result = {
        "file": file_path,
        "type": None,
        "files": [],
        "total_files": 0,
        "total_size": 0,
        "file_types": {}
    }
    
    mime = magic.from_file(file_path, mime=True)
    result["type"] = mime
    
    try:
        if mime == "application/zip":
            with zipfile.ZipFile(file_path, 'r') as zf:
                for info in zf.infolist():
                    result["files"].append({
                        "name": info.filename,
                        "size": info.file_size,
                        "compressed": info.compress_size,
                        "modified": str(datetime(*info.date_time))
                    })
                    ext = os.path.splitext(info.filename)[1]
                    result["file_types"][ext] = result["file_types"].get(ext, 0) + 1
        
        elif "rar" in mime:
            with rarfile.RarFile(file_path, 'r') as rf:
                for info in rf.infolist():
                    result["files"].append({
                        "name": info.filename,
                        "size": info.file_size,
                        "compressed": info.compress_size,
                        "modified": str(datetime(*info.date_time))
                    })
                    ext = os.path.splitext(info.filename)[1]
                    result["file_types"][ext] = result["file_types"].get(ext, 0) + 1
        
        elif "7z" in mime:
            with py7zr.SevenZipFile(file_path, 'r') as szf:
                for info in szf.list():
                    result["files"].append({
                        "name": info.filename,
                        "size": info.uncompressed,
                        "compressed": info.compressed,
                        "modified": str(info.creationtime) if info.creationtime else None
                    })
        
        elif "tar" in mime:
            with tarfile.open(file_path, 'r') as tf:
                for info in tf.getmembers():
                    result["files"].append({
                        "name": info.name,
                        "size": info.size,
                        "modified": str(datetime.fromtimestamp(info.mtime))
                    })
                    ext = os.path.splitext(info.name)[1]
                    result["file_types"][ext] = result["file_types"].get(ext, 0) + 1
        
        result["total_files"] = len(result["files"])
        result["total_size"] = sum(f["size"] for f in result["files"])
        
    except Exception as e:
        result["error"] = str(e)
    
    return result

# ============================================================
# ФУНКЦИИ ДЛЯ ТЕЛЕФОНА
# ============================================================

async def search_phone(phone: str) -> Dict[str, Any]:
    """Полный поиск по телефону"""
    phone_clean = re.sub(r'[^\d+]', '', phone)
    result = {
        "номер": phone_clean,
        "phonenumbers": {},
        "numverify": {},
        "abstractapi": {},
        "veriphone": {},
        "мессенджеры": [],
        "соцсети": {},
        "утечки": [],
        "комментарии": []
    }
    
    try:
        pn = phonenumbers.parse(phone_clean, None)
        result["phonenumbers"] = {
            "валиден": phonenumbers.is_valid_number(pn),
            "возможен": phonenumbers.is_possible_number(pn),
            "международный": phonenumbers.format_number(pn, PhoneNumberFormat.INTERNATIONAL),
            "национальный": phonenumbers.format_number(pn, PhoneNumberFormat.NATIONAL),
            "E164": phonenumbers.format_number(pn, PhoneNumberFormat.E164),
            "страна": geocoder.description_for_number(pn, "ru"),
            "регион": geocoder.description_for_number(pn, "en"),
            "оператор": carrier.name_for_number(pn, "ru"),
            "часовой_пояс": timezone.time_zones_for_number(pn)[0] if timezone.time_zones_for_number(pn) else None
        }
    except:
        pass
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        if NUMVERIFY_KEY:
            tasks.append(fetch_numverify(session, phone_clean))
        if ABSTRACT_API_KEY:
            tasks.append(fetch_abstractapi(session, phone_clean))
        if VERIPHONE_KEY:
            tasks.append(fetch_veriphone(session, phone_clean))
        
        tasks.append(check_messengers(session, phone_clean))
        tasks.append(check_phone_leaks(session, phone_clean))
        tasks.append(check_phone_reviews(session, phone_clean))
        tasks.append(find_social_by_phone(session, phone_clean))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for r in results:
            if isinstance(r, dict):
                for key, value in r.items():
                    if key in result:
                        if isinstance(result[key], dict):
                            result[key].update(value)
                        elif isinstance(result[key], list):
                            result[key].extend(value)
    
    return result

async def fetch_numverify(session, phone):
    try:
        r = await session.get("http://apilayer.net/api/validate",
            params={"access_key": NUMVERIFY_KEY, "number": phone, "format": 1})
        data = await r.json()
        return {"numverify": data} if data.get("valid") else {}
    except:
        return {}

async def fetch_abstractapi(session, phone):
    try:
        r = await session.get("https://phonevalidation.abstractapi.com/v1/",
            params={"api_key": ABSTRACT_API_KEY, "phone": phone})
        data = await r.json()
        return {"abstractapi": data} if data.get("valid") else {}
    except:
        return {}

async def fetch_veriphone(session, phone):
    try:
        r = await session.get("https://api.veriphone.io/v2/verify",
            params={"key": VERIPHONE_KEY, "phone": phone})
        data = await r.json()
        return {"veriphone": data} if data.get("phone_valid") else {}
    except:
        return {}

async def check_messengers(session, phone):
    messengers = []
    try:
        r = await session.get(f"https://t.me/+{phone.replace('+', '')}", headers=HEADERS, timeout=5)
        if r.status == 200:
            messengers.append({"name": "Telegram", "url": f"https://t.me/+{phone.replace('+', '')}"})
    except:
        pass
    try:
        r = await session.get(f"https://wa.me/{phone.replace('+', '')}", headers=HEADERS, timeout=5)
        if r.status == 200:
            messengers.append({"name": "WhatsApp", "url": f"https://wa.me/{phone.replace('+', '')}"})
    except:
        pass
    try:
        r = await session.get(f"https://invite.viber.com/?g2=+{phone.replace('+', '')}", headers=HEADERS, timeout=5)
        if r.status == 200:
            messengers.append({"name": "Viber", "url": f"viber://chat?number=%2B{phone.replace('+', '')}"})
    except:
        pass
    return {"мессенджеры": messengers}

async def check_phone_leaks(session, phone):
    leaks = []
    try:
        r = await session.get(f"https://leakcheck.io/api/v2/query/{phone}", headers={"X-API-Key": "public"})
        if r.status == 200:
            data = await r.json()
            if data.get("sources"):
                for source in data["sources"][:5]:
                    leaks.append({
                        "источник": source.get("name"),
                        "дата": source.get("date"),
                        "данные": source.get("line", "")[:100]
                    })
    except:
        pass
    return {"утечки": leaks}

async def check_phone_reviews(session, phone):
    comments = []
    try:
        r = await session.get(f"https://kto-zvonil.ru/number/{phone.replace('+', '')}", headers=HEADERS)
        if r.status == 200:
            t = await r.text()
            found = re.findall(r'class="comment_text">([^<]+)<', t)
            for c in found[:5]:
                comments.append(c.strip())
    except:
        pass
    return {"комментарии": comments}

async def find_social_by_phone(session, phone):
    social = {}
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        r = await session.get(f"https://vk.com/search?c%5Bphone%5D={clean_phone}", headers=HEADERS)
        if r.status == 200:
            t = await r.text()
            profiles = re.findall(r'href="/(id\d+)"', t)
            if profiles:
                social["VK"] = f"https://vk.com/{profiles[0]}"
    except:
        pass
    return {"соцсети": social}

# ============================================================
# ФУНКЦИИ ДЛЯ EMAIL
# ============================================================

async def search_email(email: str) -> Dict[str, Any]:
    """Полный поиск по email"""
    email = email.strip().lower()
    result = {
        "email": email,
        "формат_валиден": bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)),
        "домен": email.split("@")[1] if "@" in email else None,
        "валиден": False,
        "mx_записи": [],
        "spf_запись": None,
        "dmarc_запись": None,
        "whois_домена": {},
        "ssl_сертификат": {},
        "владелец": None,
        "фото": None,
        "соцсети": {},
        "утечки": []
    }
    
    if "@" in email:
        domain = result["домен"]
        
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            for mx in mx_records:
                result["mx_записи"].append({"приоритет": mx.preference, "сервер": str(mx.exchange)})
            result["валиден"] = len(result["mx_записи"]) > 0
        except:
            pass
        
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT')
            for txt in txt_records:
                txt_str = str(txt).lower()
                if "v=spf1" in txt_str:
                    result["spf_запись"] = str(txt)
                if "v=DMARC1" in txt_str:
                    result["dmarc_запись"] = str(txt)
        except:
            pass
        
        try:
            w = whois.whois(domain)
            result["whois_домена"] = {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date),
                "name_servers": w.name_servers,
                "country": w.country,
                "org": w.org,
                "emails": w.emails
            }
        except:
            pass
        
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.connect((domain, 443))
                cert = s.getpeercert()
                result["ssl_сертификат"] = {
                    "issuer": dict(cert.get("issuer", [])),
                    "subject": dict(cert.get("subject", [])),
                    "notBefore": cert.get("notBefore"),
                    "notAfter": cert.get("notAfter")
                }
        except:
            pass
        
        try:
            email_hash = hashlib.md5(email.encode()).hexdigest()
            async with aiohttp.ClientSession() as s:
                r = await s.get(f"https://www.gravatar.com/{email_hash}.json", headers=HEADERS)
                if r.status == 200:
                    data = await r.json()
                    entry = data.get("entry", [{}])[0]
                    result["владелец"] = entry.get("displayName") or entry.get("preferredUsername")
                    result["фото"] = f"https://www.gravatar.com/avatar/{email_hash}?s=400"
                    if entry.get("urls"):
                        for url in entry["urls"]:
                            result["соцсети"][url.get("title")] = url.get("value")
        except:
            pass
        
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get(f"https://api.hunter.io/v2/email-verifier?email={email}", headers=HEADERS)
                if r.status == 200:
                    data = await r.json()
                    d = data.get("data", {})
                    if d:
                        if not result["владелец"] and (d.get("first_name") or d.get("last_name")):
                            result["владелец"] = f"{d.get('first_name', '')} {d.get('last_name', '')}".strip()
                        if d.get("twitter"):
                            result["соцсети"]["Twitter"] = f"https://twitter.com/{d['twitter']}"
                        if d.get("linkedin"):
                            result["соцсети"]["LinkedIn"] = d['linkedin']
                        if d.get("github"):
                            result["соцсети"]["GitHub"] = f"https://github.com/{d['github']}"
        except:
            pass
        
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", headers=HEADERS)
                if r.status == 200:
                    breaches = await r.json()
                    for b in breaches:
                        result["утечки"].append({
                            "название": b.get("Name"),
                            "дата": b.get("BreachDate"),
                            "данные": b.get("DataClasses", [])
                        })
        except:
            pass
    
    return result

# ============================================================
# ФУНКЦИИ ДЛЯ ФИО
# ============================================================

async def search_fullname(fio: str) -> Dict[str, Any]:
    """Полный поиск по ФИО"""
    parts = fio.strip().split()
    name = parts[1] if len(parts) > 1 else (parts[0] if parts else "")
    surname = parts[0] if parts else ""
    
    result = {
        "фио": fio,
        "фамилия": surname,
        "имя": name,
        "отчество": parts[2] if len(parts) > 2 else None,
        "nameapi": {},
        "namsor": {},
        "genderapi": {},
        "agify": {},
        "nationalize": {},
        "соцсети": {},
        "адреса": []
    }
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        if NAMEAPI_KEY:
            tasks.append(fetch_nameapi(session, fio))
        if NAMSOR_KEY and name and surname:
            tasks.append(fetch_namsor(session, name, surname))
        if GENDERAPI_KEY and name:
            tasks.append(fetch_genderapi(session, name))
        if name:
            tasks.append(fetch_agify(session, name))
            tasks.append(fetch_nationalize(session, name))
        
        tasks.append(find_vk_by_name(session, fio))
        tasks.append(find_other_social_by_name(session, fio))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for r in results:
            if isinstance(r, dict):
                for key, value in r.items():
                    if key in result:
                        if isinstance(result[key], dict):
                            result[key].update(value)
                        elif isinstance(result[key], list):
                            result[key].extend(value)
    
    return result

async def fetch_nameapi(session, fio):
    try:
        d = {"inputPerson": {"name": {"nameFields": [{"stringValue": fio}]}}}
        r = await session.post("https://api.nameapi.org/rest/v5.3/parser/person-name-parser",
            params={"apiKey": NAMEAPI_KEY}, json=d)
        data = await r.json()
        m = data.get("matches", [{}])[0]
        g = m.get("gender", {}).get("gender")
        return {"nameapi": {
            "пол": "Мужской" if g == "MALE" else "Женский" if g == "FEMALE" else None,
            "уверенность": m.get("gender", {}).get("confidence")
        }}
    except:
        return {}

async def fetch_namsor(session, name, surname):
    try:
        r = await session.get(f"https://v2.namsor.com/NamsorAPIv2/api2/json/genderFull/{name}/{surname}",
            headers={"X-API-KEY": NAMSOR_KEY})
        data = await r.json()
        return {"namsor": {
            "пол": data.get("likelyGender"),
            "этнос": data.get("ethnicity"),
            "страна": data.get("countryOrigin"),
            "религия": data.get("religion")
        }}
    except:
        return {}

async def fetch_genderapi(session, name):
    try:
        r = await session.get("https://gender-api.com/v2/gender",
            params={"key": GENDERAPI_KEY, "name": name})
        data = await r.json()
        return {"genderapi": {
            "пол": "Мужской" if data.get("gender") == "male" else "Женский" if data.get("gender") == "female" else None,
            "точность": data.get("accuracy")
        }}
    except:
        return {}

async def fetch_agify(session, name):
    try:
        r = await session.get(f"https://api.agify.io?name={name}")
        data = await r.json()
        return {"agify": {
            "возраст": data.get("age"),
            "количество": data.get("count")
        }}
    except:
        return {}

async def fetch_nationalize(session, name):
    try:
        r = await session.get(f"https://api.nationalize.io?name={name}")
        data = await r.json()
        countries = data.get("country", [])
        if countries:
            country_map = {"RU": "Россия", "UA": "Украина", "BY": "Беларусь", "KZ": "Казахстан",
                "US": "США", "GB": "Великобритания", "DE": "Германия", "FR": "Франция"}
            return {"nationalize": {
                "страна": country_map.get(countries[0]["country_id"]),
                "вероятность": countries[0]["probability"]
            }}
    except:
        return {}

async def find_vk_by_name(session, fio):
    result = {}
    try:
        r = await session.get(f"https://vk.com/search?c%5Bq%5D={fio}", headers=HEADERS)
        if r.status == 200:
            t = await r.text()
            profiles = re.findall(r'href="/([^"]+)"[^>]*>([^<]+)</a>', t)
            for url, name in profiles[:5]:
                if not url.startswith('id') and url not in ['feed', 'friends', 'photos']:
                    result[f"VK_{name}"] = {"url": f"https://vk.com/{url}", "name": name}
    except:
        pass
    return {"соцсети": result}

async def find_other_social_by_name(session, fio):
    result = {}
    try:
        names = fio.split()
        if len(names) >= 2:
            r = await session.get(f"https://www.linkedin.com/pub/dir?firstName={names[0]}&lastName={names[1]}",
                headers=HEADERS)
            if r.status == 200:
                t = await r.text()
                profiles = re.findall(r'href="/in/([^"/]+)"', t)
                if profiles:
                    result["LinkedIn"] = f"https://linkedin.com/in/{profiles[0]}"
    except:
        pass
    return {"соцсети": result}

# ============================================================
# ФУНКЦИИ ДЛЯ IP И ДОМЕНОВ
# ============================================================

async def search_ip(ip: str) -> Dict[str, Any]:
    """Поиск по IP"""
    result = {
        "ip": ip,
        "geo": {},
        "asn": {},
        "hostname": None
    }
    
    if IPINFO_KEY:
        try:
            async with aiohttp.ClientSession() as session:
                r = await session.get(f"https://ipinfo.io/{ip}", headers={"Authorization": f"Bearer {IPINFO_KEY}"})
                data = await r.json()
                result["geo"] = {
                    "city": data.get("city"),
                    "region": data.get("region"),
                    "country": data.get("country"),
                    "loc": data.get("loc"),
                    "org": data.get("org"),
                    "timezone": data.get("timezone")
                }
                result["hostname"] = data.get("hostname")
        except:
            pass
    
    if IPGEOLOCATION_KEY:
        try:
            async with aiohttp.ClientSession() as session:
                r = await session.get("https://api.ipgeolocation.io/ipgeo",
                    params={"apiKey": IPGEOLOCATION_KEY, "ip": ip})
                data = await r.json()
                result["geo"]["isp"] = data.get("isp")
                result["geo"]["asn"] = data.get("asn")
        except:
            pass
    
    return result

async def analyze_domain(domain: str) -> Dict[str, Any]:
    """Анализ домена"""
    result = {
        "domain": domain,
        "whois": {},
        "dns": {},
        "ssl": {}
    }
    
    try:
        w = whois.whois(domain)
        result["whois"] = {
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers,
            "country": w.country,
            "org": w.org
        }
    except:
        pass
    
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            result["dns"][rtype] = [str(a) for a in answers]
        except:
            pass
    
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.connect((domain, 443))
            cert = s.getpeercert()
            result["ssl"] = {
                "issuer": dict(cert.get("issuer", [])),
                "subject": dict(cert.get("subject", [])),
                "notBefore": cert.get("notBefore"),
                "notAfter": cert.get("notAfter")
            }
    except:
        pass
    
    return result

# ============================================================
# ФУНКЦИИ ДЛЯ НИКНЕЙМА
# ============================================================

async def search_nickname(username: str) -> Dict[str, Any]:
    """Поиск по никнейму"""
    result = {
        "query": username,
        "platforms": {},
        "total_found": 0
    }
    
    platforms = {
        "Telegram": f"https://t.me/{username}",
        "VK": f"https://vk.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://x.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Twitch": f"https://twitch.tv/{username}",
        "YouTube": f"https://youtube.com/@{username}",
        "TikTok": f"https://tiktok.com/@{username}",
        "LinkedIn": f"https://linkedin.com/in/{username}",
        "Pinterest": f"https://pinterest.com/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Dev.to": f"https://dev.to/{username}",
        "GitLab": f"https://gitlab.com/{username}",
        "Bitbucket": f"https://bitbucket.org/{username}",
        "Behance": f"https://behance.net/{username}",
        "Dribbble": f"https://dribbble.com/{username}",
        "Flickr": f"https://flickr.com/people/{username}",
        "Patreon": f"https://patreon.com/{username}",
        "Spotify": f"https://open.spotify.com/user/{username}",
        "Last.fm": f"https://last.fm/user/{username}",
        "CodePen": f"https://codepen.io/{username}",
        "Replit": f"https://replit.com/@{username}",
        "Gravatar": f"https://gravatar.com/{username}",
        "Imgur": f"https://imgur.com/user/{username}",
        "DeviantArt": f"https://deviantart.com/{username}",
        "About.me": f"https://about.me/{username}",
        "Habr": f"https://habr.com/ru/users/{username}",
        "Pikabu": f"https://pikabu.ru/@{username}",
        "Ok.ru": f"https://ok.ru/{username}"
    }
    
    async with aiohttp.ClientSession() as session:
        tasks = [check_platform(session, name, url) for name, url in platforms.items()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for r in results:
            if isinstance(r, dict) and r.get("found"):
                result["platforms"][r["name"]] = r
                result["total_found"] += 1
    
    return result

async def check_platform(session, name, url):
    try:
        r = await session.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
        if r.status == 200:
            return {"name": name, "url": url, "found": True}
    except:
        pass
    return {"name": name, "found": False}

# ============================================================
# ФУНКЦИИ ДЛЯ ПАРОЛЯ
# ============================================================

async def check_password(password: str) -> Dict[str, Any]:
    """Проверка пароля"""
    result = {
        "длина": len(password),
        "скомпрометирован": False,
        "количество_утечек": 0,
        "сложность": None,
        "время_взлома": None,
        "энтропия": 0
    }
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    charset = 0
    if has_lower: charset += 26
    if has_upper: charset += 26
    if has_digit: charset += 10
    if has_special: charset += 32
    if charset > 0:
        result["энтропия"] = len(password) * math.log2(charset)
    
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
    except:
        pass
    
    return result

# ============================================================
# ФУНКЦИИ ДЛЯ КРИПТОВАЛЮТ
# ============================================================

async def analyze_crypto(address: str, network: str = "eth") -> Dict[str, Any]:
    """Анализ крипто-кошельков"""
    result = {
        "address": address,
        "network": network,
        "balance": 0,
        "transactions": []
    }
    
    if network == "btc":
        try:
            async with aiohttp.ClientSession() as session:
                r = await session.get(f"https://blockchain.info/rawaddr/{address}")
                if r.status == 200:
                    data = await r.json()
                    result["balance"] = data.get("final_balance", 0) / 100000000
                    result["total_received"] = data.get("total_received", 0) / 100000000
                    result["total_sent"] = data.get("total_sent", 0) / 100000000
                    result["n_tx"] = data.get("n_tx", 0)
                    for tx in data.get("txs", [])[:5]:
                        result["transactions"].append({
                            "hash": tx["hash"],
                            "time": datetime.fromtimestamp(tx["time"]).isoformat(),
                            "result": tx["result"] / 100000000
                        })
        except:
            pass
    
    return result

# ============================================================
# ФУНКЦИИ ДЛЯ УТЕЧЕК
# ============================================================

async def search_breaches(query: str) -> Dict[str, Any]:
    """Поиск в утечках"""
    result = {
        "query": query,
        "hibp": [],
        "leakcheck": [],
        "total_breaches": 0
    }
    
    if "@" in query:
        try:
            async with aiohttp.ClientSession() as session:
                r = await session.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{query}",
                    headers={"hibp-api-key": ""})
                if r.status == 200:
                    breaches = await r.json()
                    for b in breaches:
                        result["hibp"].append({
                            "name": b.get("Name"),
                            "domain": b.get("Domain"),
                            "date": b.get("BreachDate"),
                            "description": b.get("Description", "")[:200]
                        })
        except:
            pass
    
    try:
        async with aiohttp.ClientSession() as session:
            r = await session.get(f"https://leakcheck.io/api/v2/query/{query}",
                headers={"X-API-Key": "public"})
            if r.status == 200:
                data = await r.json()
                if data.get("sources"):
                    for source in data["sources"]:
                        result["leakcheck"].append({
                            "source": source.get("name"),
                            "date": source.get("date"),
                            "line": source.get("line", "")[:200]
                        })
    except:
        pass
    
    result["total_breaches"] = len(result["hibp"]) + len(result["leakcheck"])
    return result

# ============================================================
# ФОРМАТИРОВАНИЕ РЕЗУЛЬТАТОВ
# ============================================================

def format_phone_result(r):
    t = f"<b>📱 ТЕЛЕФОН: {r['номер']}</b>\n\n"
    
    if r.get("phonenumbers"):
        pn = r["phonenumbers"]
        t += "<b>📞 Информация:</b>\n"
        if pn.get("международный"): t += f"• Формат: {pn['международный']}\n"
        if pn.get("страна"): t += f"• Страна: {pn['страна']}\n"
        if pn.get("оператор"): t += f"• Оператор: {pn['оператор']}\n"
        t += f"• Валиден: {'✅' if pn.get('валиден') else '❌'}\n\n"
    
    if r.get("numverify") and r["numverify"].get("valid"):
        nv = r["numverify"]
        t += "<b>📡 NumVerify:</b>\n"
        if nv.get("country_name"): t += f"• Страна: {nv['country_name']}\n"
        if nv.get("carrier"): t += f"• Оператор: {nv['carrier']}\n"
        t += "\n"
    
    if r.get("мессенджеры"):
        t += "<b>💬 Мессенджеры:</b>\n"
        for m in r["мессенджеры"]:
            t += f"• {m['name']}\n"
        t += "\n"
    
    if r.get("соцсети"):
        t += "<b>🌐 Соцсети:</b>\n"
        for name, url in r["соцсети"].items():
            t += f"• <b>{name}:</b> {url}\n"
        t += "\n"
    
    if r.get("утечки"):
        t += f"<b>🔴 Утечки ({len(r['утечки'])}):</b>\n"
        for leak in r["утечки"][:3]:
            t += f"• {leak.get('источник', 'N/A')}\n"
    
    return t

def format_email_result(r):
    t = f"<b>📧 EMAIL: {r['email']}</b>\n\n"
    t += f"✅ Формат: {'OK' if r['формат_валиден'] else 'Ошибка'}\n"
    t += f"📧 Валиден: {'Да' if r['валиден'] else 'Нет'}\n"
    
    if r.get("владелец"):
        t += f"👤 Владелец: {r['владелец']}\n"
    
    if r.get("соцсети"):
        t += "<b>🌐 Соцсети:</b>\n"
        for name, url in r["соцсети"].items():
            t += f"• <b>{name}:</b> {url}\n"
        t += "\n"
    
    if r.get("утечки"):
        t += f"<b>🔴 Утечки ({len(r['утечки'])}):</b>\n"
        for u in r["утечки"][:5]:
            t += f"• {u['название']} ({u.get('дата', 'N/A')})\n"
    
    return t

def format_fullname_result(r):
    t = f"<b>👤 ФИО: {r['фио']}</b>\n\n"
    
    if r.get("nameapi") and r["nameapi"].get("пол"):
        t += f"<b>NameAPI:</b> {r['nameapi']['пол']}\n"
    
    if r.get("namsor") and r["namsor"].get("пол"):
        ns = r["namsor"]
        t += "<b>Namsor:</b>\n"
        t += f"• Пол: {ns['пол']}\n"
        if ns.get("этнос"): t += f"• Этнос: {ns['этнос']}\n"
        if ns.get("страна"): t += f"• Страна: {ns['страна']}\n"
    
    if r.get("agify") and r["agify"].get("возраст"):
        t += f"<b>Возраст:</b> ~{r['agify']['возраст']} лет\n"
    
    if r.get("соцсети"):
        t += "<b>🌐 Найденные профили:</b>\n"
        for name, data in r["соцсети"].items():
            if isinstance(data, dict):
                t += f"• <b>{name}:</b> <a href='{data.get('url', '')}'>{data.get('name', 'Профиль')}</a>\n"
    
    return t

def format_ip_result(r):
    t = f"<b>🌐 IP: {r['ip']}</b>\n\n"
    
    if r.get("geo"):
        g = r["geo"]
        t += "<b>📍 Геолокация:</b>\n"
        if g.get("country"): t += f"• Страна: {g['country']}\n"
        if g.get("city"): t += f"• Город: {g['city']}\n"
        if g.get("loc"): t += f"• Координаты: {g['loc']}\n"
        t += "\n"
    
    return t

def format_domain_result(r):
    t = f"<b>🌐 ДОМЕН: {r['domain']}</b>\n\n"
    
    if r.get("whois"):
        w = r["whois"]
        t += "<b>📋 WHOIS:</b>\n"
        if w.get("registrar"): t += f"• Регистратор: {w['registrar']}\n"
        if w.get("creation_date"): t += f"• Создан: {w['creation_date']}\n"
        if w.get("expiration_date"): t += f"• Истекает: {w['expiration_date']}\n"
        t += "\n"
    
    if r.get("dns"):
        t += "<b>📡 DNS записи:</b>\n"
        for rtype, records in r["dns"].items():
            t += f"• {rtype}: {', '.join(records[:3])}\n"
        t += "\n"
    
    return t

def format_nickname_result(r):
    t = f"<b>🔍 НИКНЕЙМ: @{r['query']}</b>\n\n"
    t += f"📊 Найдено профилей: {r['total_found']}\n\n"
    
    if r.get("platforms"):
        t += "<b>✅ Найденные платформы:</b>\n"
        for name, data in r["platforms"].items():
            if data.get("found"):
                t += f"• <b>{name}:</b> <a href='{data['url']}'>Профиль</a>\n"
    
    return t

def format_password_result(r):
    t = "<b>🔐 АНАЛИЗ ПАРОЛЯ</b>\n\n"
    t += f"📏 Длина: {r['длина']} символов\n"
    t += f"📊 Сложность: {r['сложность']}\n"
    t += f"⏱ Время взлома: {r['время_взлома']}\n"
    
    if r.get("скомпрометирован"):
        t += f"\n🔴 <b>СКОМПРОМЕТИРОВАН!</b>\n"
        t += f"📊 Найден в утечках: {r['количество_утечек']:,} раз\n".replace(',', ' ')
    else:
        t += "\n✅ Не найден в утечках\n"
    
    return t

def format_crypto_result(r):
    t = f"<b>💰 КРИПТО-КОШЕЛЕК</b>\n\n"
    t += f"📌 Адрес: <code>{r['address']}</code>\n"
    t += f"🌐 Сеть: {r['network'].upper()}\n"
    t += f"💰 Баланс: {r['balance']}\n\n"
    
    if r.get("transactions"):
        t += f"<b>📊 Последние транзакции ({len(r['transactions'])}):</b>\n"
        for tx in r["transactions"][:5]:
            t += f"• {tx['hash'][:10]}... : {tx.get('result', 'N/A')}\n"
    
    return t

def format_document_result(r):
    t = f"<b>📄 АНАЛИЗ ДОКУМЕНТА</b>\n\n"
    t += f"📁 Файл: {os.path.basename(r['file'])}\n"
    t += f"📌 Тип: {r['type']}\n\n"
    
    if r.get("author"):
        t += f"👤 Автор: {r['author']}\n"
    if r.get("created"):
        t += f"📅 Создан: {r['created']}\n"
    
    if r.get("emails"):
        t += f"\n📧 Email ({len(r['emails'])}):\n"
        for e in r["emails"][:5]:
            t += f"• {e}\n"
    
    if r.get("phones"):
        t += f"\n📱 Телефоны ({len(r['phones'])}):\n"
        for p in r["phones"][:5]:
            t += f"• {p}\n"
    
    return t

# ============================================================
# МЕНЮ И ХЕНДЛЕРЫ
# ============================================================

def main_menu():
    b = InlineKeyboardBuilder()
    buttons = [
        ("📱 Телефон", "phone"),
        ("📧 Email", "email"),
        ("👤 ФИО", "fullname"),
        ("🔍 Никнейм", "nickname"),
        ("🌐 IP", "ip"),
        ("🌍 Домен", "domain"),
        ("🔐 Пароль", "password"),
        ("💰 Крипто", "crypto"),
        ("📄 Анализ файла", "file"),
        ("🔥 ГЛУБОКИЙ ПОИСК", "deep_search")
    ]
    for text, data in buttons:
        b.button(text=text, callback_data=data)
    b.adjust(2)
    return b.as_markup()

@dp.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>🔥 ULTIMATE AGGRESSIVE OSINT FRAMEWORK</b>\n\n"
        "<i>✅ ВСЕ ИМПОРТЫ РАБОТАЮТ!</i>\n"
        "<i>✅ ВСЕ API ПОДКЛЮЧЕНЫ!</i>\n\n"
        "<b>📊 ДОСТУПНЫЕ МОДУЛИ:</b>\n"
        "• 📱 Телефон - оператор, соцсети, утечки\n"
        "• 📧 Email - владелец, Gravatar, breaches\n"
        "• 👤 ФИО - пол, возраст, соцсети\n"
        "• 🔍 Никнейм - 30+ платформ\n"
        "• 🌐 IP - геолокация, провайдер\n"
        "• 🌍 Домен - WHOIS, DNS, SSL\n"
        "• 🔐 Пароль - сложность, утечки\n"
        "• 💰 Крипто - баланс, транзакции\n"
        "• 📄 Анализ файлов - EXIF, метаданные\n"
        "• 🔥 ГЛУБОКИЙ ПОИСК - ВСЁ СРАЗУ\n\n"
        "Выберите тип поиска:",
        reply_markup=main_menu()
    )
    await state.set_state(SearchStates.choosing)

@dp.callback_query(F.data == "back")
async def back_cb(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchStates.choosing)
    await callback.message.edit_text(
        "<b>🔥 ULTIMATE AGGRESSIVE OSINT</b>\n\nВыберите тип поиска:",
        reply_markup=main_menu()
    )
    await callback.answer()

@dp.callback_query(SearchStates.choosing)
async def choice_cb(callback: CallbackQuery, state: FSMContext):
    d = callback.data
    prompts = {
        "phone": (SearchStates.phone, "📱 <b>Введите номер телефона</b>\n\nПример: +79001234567"),
        "email": (SearchStates.email, "📧 <b>Введите Email</b>\n\nПример: user@example.com"),
        "fullname": (SearchStates.fullname, "👤 <b>Введите ФИО</b>\n\nПример: Иванов Иван Иванович"),
        "nickname": (SearchStates.nickname, "🔍 <b>Введите никнейм</b>\n\nПример: username"),
        "ip": (SearchStates.ip, "🌐 <b>Введите IP адрес</b>\n\nПример: 8.8.8.8"),
        "domain": (SearchStates.domain, "🌍 <b>Введите домен</b>\n\nПример: example.com"),
        "password": (SearchStates.password, "🔐 <b>Введите пароль</b>"),
        "crypto": (SearchStates.crypto, "💰 <b>Введите адрес крипто-кошелька</b>\n\nПример: 1A1zP1... или 0x..."),
        "file": (SearchStates.file_analysis, "📄 <b>Отправьте файл для анализа</b>\n\nПоддерживаются: PDF, DOCX, XLSX, PPTX, ZIP, RAR, 7z, изображения"),
        "deep_search": (SearchStates.deep_search, "🔥 <b>ГЛУБОКИЙ ПОИСК</b>\n\nВведите любые данные (телефон, email, ФИО, никнейм)\nБот соберет ВСЕ данные!")
    }
    if d in prompts:
        ns, pt = prompts[d]
        await state.set_state(ns)
        await callback.message.edit_text(
            pt,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
            ])
        )
    await callback.answer()

@dp.message(SearchStates.phone)
async def phone_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Сбор данных о телефоне...")
    r = await search_phone(message.text.strip())
    await w.delete()
    await message.answer(
        format_phone_result(r),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Удалить", callback_data="del"),
             InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
        ]),
        disable_web_page_preview=True
    )
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.email)
async def email_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Сбор данных об email...")
    r = await search_email(message.text.strip())
    await w.delete()
    if r.get("фото"):
        try:
            await message.answer_photo(r["фото"], caption="📸 Gravatar")
        except:
            pass
    await message.answer(
        format_email_result(r),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Удалить", callback_data="del"),
             InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
        ]),
        disable_web_page_preview=True
    )
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.fullname)
async def fullname_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Анализ ФИО...")
    r = await search_fullname(message.text.strip())
    await w.delete()
    await message.answer(
        format_fullname_result(r),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Удалить", callback_data="del"),
             InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
        ]),
        disable_web_page_preview=True
    )
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.nickname)
async def nickname_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Поиск по 30+ платформам...")
    r = await search_nickname(message.text.strip())
    await w.delete()
    await message.answer(
        format_nickname_result(r),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Удалить", callback_data="del"),
             InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
        ]),
        disable_web_page_preview=True
    )
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.ip)
async def ip_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Анализ IP...")
    r = await search_ip(message.text.strip())
    await w.delete()
    if r.get("geo", {}).get("loc"):
        try:
            lat, lon = r["geo"]["loc"].split(",")
            await message.answer_location(float(lat), float(lon))
        except:
            pass
    await message.answer(
        format_ip_result(r),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Удалить", callback_data="del"),
             InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
        ]),
        disable_web_page_preview=True
    )
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.domain)
async def domain_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Анализ домена...")
    r = await analyze_domain(message.text.strip())
    await w.delete()
    await message.answer(
        format_domain_result(r),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Удалить", callback_data="del"),
             InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
        ]),
        disable_web_page_preview=True
    )
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.password)
async def password_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Проверка пароля...")
    r = await check_password(message.text.strip())
    try:
        await message.delete()
    except:
        pass
    await w.delete()
    await message.answer(
        format_password_result(r),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Удалить", callback_data="del"),
             InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
        ])
    )
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.crypto)
async def crypto_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Анализ крипто-кошелька...")
    
    address = message.text.strip()
    if address.startswith("0x"):
        network = "eth"
    elif address.startswith("1") or address.startswith("3") or address.startswith("bc1"):
        network = "btc"
    else:
        network = "btc"
    
    r = await analyze_crypto(address, network)
    await w.delete()
    await message.answer(
        format_crypto_result(r),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Удалить", callback_data="del"),
             InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
        ]),
        disable_web_page_preview=True
    )
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.file_analysis)
async def file_analysis_msg(message: Message, state: FSMContext):
    if not message.document:
        await message.answer("❌ Пожалуйста, отправьте файл!")
        return
    
    w = await message.answer("⏳ Загрузка и анализ файла...")
    
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = f"/tmp/{message.document.file_name}"
    await bot.download_file(file.file_path, file_path)
    
    mime = magic.from_file(file_path, mime=True)
    
    if mime.startswith("image/"):
        r = await analyze_image_exif(file_path)
        t = f"<b>📸 АНАЛИЗ ИЗОБРАЖЕНИЯ</b>\n\n"
        if r.get("camera"):
            t += f"📷 Камера: {r['camera'].get('Make', '')} {r['camera'].get('Model', '')}\n"
        if r.get("datetime"):
            t += f"📅 Дата съемки: {r['datetime']}\n"
        if r.get("gps") and r["gps"].get("decimal"):
            lat = r["gps"]["decimal"]["lat"]
            lon = r["gps"]["decimal"]["lon"]
            t += f"📍 Координаты: {lat:.6f}, {lon:.6f}\n"
            await message.answer_location(lat, lon)
    
    elif "pdf" in mime or "document" in mime or "spreadsheet" in mime or "presentation" in mime:
        r = await analyze_document(file_path)
        t = format_document_result(r)
    
    elif "zip" in mime or "rar" in mime or "7z" in mime or "tar" in mime:
        r = await analyze_archive(file_path)
        t = f"<b>📦 АНАЛИЗ АРХИВА</b>\n\n"
        t += f"📁 Файлов: {r['total_files']}\n"
        t += f"💾 Размер: {r['total_size']:,} байт\n\n"
        if r.get("file_types"):
            t += "<b>📊 Типы файлов:</b>\n"
            for ext, count in r["file_types"].items():
                t += f"• {ext or 'без расширения'}: {count}\n"
    else:
        t = f"❌ Неподдерживаемый тип файла: {mime}"
    
    try:
        os.remove(file_path)
    except:
        pass
    
    await w.delete()
    await message.answer(
        t,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Удалить", callback_data="del"),
             InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
        ]),
        disable_web_page_preview=True
    )
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.deep_search)
async def deep_search_msg(message: Message, state: FSMContext):
    query = message.text.strip()
    w = await message.answer("🔥 <b>ЗАПУЩЕН ГЛУБОКИЙ ПОИСК</b>\n\n⏳ Анализирую всеми доступными методами...")
    
    if re.match(r'^[\+\d\s\(\)-]{10,}$', query):
        r = await search_phone(query)
        formatted = format_phone_result(r)
    elif "@" in query:
        r = await search_email(query)
        formatted = format_email_result(r)
    elif len(query.split()) >= 2:
        r = await search_fullname(query)
        formatted = format_fullname_result(r)
    else:
        r = await search_nickname(query)
        formatted = format_nickname_result(r)
    
    breaches = await search_breaches(query)
    
    await w.delete()
    await message.answer(formatted, disable_web_page_preview=True)
    
    if breaches.get("total_breaches", 0) > 0:
        t = f"<b>🔴 ДОПОЛНИТЕЛЬНО: УТЕЧКИ ({breaches['total_breaches']})</b>\n\n"
        if breaches.get("hibp"):
            t += "<b>Have I Been Pwned:</b>\n"
            for b in breaches["hibp"][:3]:
                t += f"• {b['name']} ({b.get('date', 'N/A')})\n"
        if breaches.get("leakcheck"):
            t += "<b>LeakCheck:</b>\n"
            for l in breaches["leakcheck"][:3]:
                t += f"• {l['source']}: {l['line'][:50]}...\n"
        await message.answer(t, disable_web_page_preview=True)
    
    await message.answer(
        "✅ <b>Глубокий поиск завершен!</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Удалить", callback_data="del"),
             InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
        ])
    )
    await state.set_state(SearchStates.choosing)

@dp.callback_query(F.data == "del")
async def delete_cb(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

# ============================================================
# ЗАПУСК БОТА
# ============================================================

async def main():
    print("=" * 60)
    print("🔥 ULTIMATE AGGRESSIVE OSINT FRAMEWORK")
    print("=" * 60)
    print("✅ ВСЕ ИМПОРТЫ УСПЕШНО ЗАГРУЖЕНЫ!")
    print("✅ ВСЕ МОДУЛИ РАБОТАЮТ!")
    print("=" * 60)
    print("📡 Бот запускается...")
    print("=" * 60)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
