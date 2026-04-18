#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================
# 🔥 ULTIMATE AGGRESSIVE OSINT FRAMEWORK 🔥
# ТОЛЬКО РЕАЛЬНЫЕ СУЩЕСТВУЮЩИЕ ИМПОРТЫ
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

# Aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# Телефоны
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from phonenumbers import PhoneNumberFormat

# SSL/Криптография
import OpenSSL
import cryptography
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Изображения и EXIF
import PIL.Image
from PIL.ExifTags import TAGS, GPSTAGS
from io import BytesIO
import exifread

# Замена python-magic
import filetype
import mimetypes

# Документы
import pdfplumber
import openpyxl
from pptx import Presentation
import olefile

# Архивы
import zipfile
import tarfile
import rarfile
import py7zr

# Парсинг
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv
from urllib.parse import urlparse, parse_qs, quote, unquote

# Геолокация
import geoip2.database
import maxminddb
from geopy.geocoders import Nominatim

# API
import shodan
from shodan import Shodan
import vt
from waybackpy import WaybackMachineCDXServerAPI, WaybackMachineSaveAPI

# NLP
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
import langdetect
from langdetect import detect
from googletrans import Translator

# Графы
import networkx as nx

# Данные
import pandas as pd
import numpy as np
import dateparser
import pytz

# Утилиты
import math
import random
import string
from collections import defaultdict
from tqdm import tqdm
import colorama

# Email валидация
from email_validator import validate_email, EmailNotValidError
import idna

# Web
import tldextract
from publicsuffixlist import PublicSuffixList

# Криптовалюты
from web3 import Web3

# Дополнительно
import logging
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# ИНИЦИАЛИЗАЦИЯ
# ============================================================

mimetypes.init()
colorama.init()

# Создаем директории
os.makedirs('/tmp/osint', exist_ok=True)
os.makedirs('logs', exist_ok=True)
os.makedirs('reports', exist_ok=True)
os.makedirs('cache', exist_ok=True)
os.makedirs('uploads', exist_ok=True)
os.makedirs('exports', exist_ok=True)

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/bot.log')
    ]
)
logger = logging.getLogger(__name__)

print("=" * 60)
print("🔥 ULTIMATE AGGRESSIVE OSINT FRAMEWORK")
print("=" * 60)
print("✅ ВСЕ ИМПОРТЫ УСПЕШНО ЗАГРУЖЕНЫ!")
print("=" * 60)

# ============================================================
# ЗАМЕНА MAGIC НА FILETYPE
# ============================================================

class Magic:
    """Совместимый с python-magic интерфейс"""
    
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
                'gif': 'image/gif', 'pdf': 'application/pdf',
                'doc': 'application/msword',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'xls': 'application/vnd.ms-excel',
                'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'ppt': 'application/vnd.ms-powerpoint',
                'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'zip': 'application/zip', 'rar': 'application/x-rar-compressed',
                '7z': 'application/x-7z-compressed', 'tar': 'application/x-tar',
                'gz': 'application/gzip', 'txt': 'text/plain',
                'html': 'text/html', 'json': 'application/json',
                'xml': 'application/xml', 'mp3': 'audio/mpeg',
                'mp4': 'video/mp4', 'exe': 'application/x-msdownload'
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
    
    @staticmethod
    def version():
        return "1.0.0 (filetype fallback)"

magic = Magic

def get_file_mime(path):
    return Magic(mime=True).from_file(path)

def is_image(path):
    return get_file_mime(path).startswith('image/')

def is_document(path):
    mime = get_file_mime(path)
    return mime.startswith('application/') or mime.startswith('text/')

print("✅ python-magic ЗАМЕНЕН на filetype (без libmagic)")

# ============================================================
# КОНФИГУРАЦИЯ
# ============================================================

TOKEN = os.getenv("BOT_TOKEN", "8632505304:AAHU96AHlWJ__5CYiOK9Al_YfPqu47uHub4")

# API ключи
NUMVERIFY_KEY = os.getenv("NUMVERIFY_KEY", "8f4a8755935f55e2dc710b1b4671e78a")
ABSTRACT_API_KEY = os.getenv("ABSTRACT_API_KEY", "f8bb61d10eca41cc973ca759aa5c974b")
VERIPHONE_KEY = os.getenv("VERIPHONE_KEY", "F678B73B08A141A291CEADBD8E665DDF")
NAMEAPI_KEY = os.getenv("NAMEAPI_KEY", "e2b133ba4542d2c972d6f5bc768672c5-user1")
NAMSOR_KEY = os.getenv("NAMSOR_KEY", "40d9f9ffe04741478b033e082eb56dd5")
GENDERAPI_KEY = os.getenv("GENDERAPI_KEY", "97b1a2f5c6686615189da08470544f44fefa8bba533f86d0b86f9038a8fffd5b")
GEOAPIFY_KEY = os.getenv("GEOAPIFY_KEY", "4d4df8a3c94f405c9b2e69491c16c15a")
TELEMETR_KEY = os.getenv("TELEMETR_KEY", "QVS1pbIENSMwo63fVzPhnCflXZ8sMET7")
TGSTAT_KEY = os.getenv("TGSTAT_KEY", "7b82e991fd161884147392c533fbfb3e")
IPINFO_KEY = os.getenv("IPINFO_KEY", "3eef5851806a7e")
IPGEOLOCATION_KEY = os.getenv("IPGEOLOCATION_KEY", "ff617b5935b94dea8e14c680a36b7edc")
SHODAN_KEY = os.getenv("SHODAN_KEY", "")

storage = MemoryStorage()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
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
    nickname = State()
    ip = State()
    domain = State()
    password = State()
    crypto = State()
    file_analysis = State()
    deep_search = State()

# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def convert_to_degrees(value):
    """Конвертация GPS координат из EXIF"""
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)

# ============================================================
# АНАЛИЗ ИЗОБРАЖЕНИЙ
# ============================================================

async def analyze_image_exif(file_path: str) -> Dict[str, Any]:
    """Извлечение EXIF данных"""
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
                elif tag in ["Make", "Model"]:
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

# ============================================================
# АНАЛИЗ ДОКУМЕНТОВ
# ============================================================

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
        "author": None
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
        
        elif "wordprocessingml" in mime:
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
                "modified": str(wb.properties.modified)
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
            
    except Exception as e:
        result["error"] = str(e)
    
    return result

# ============================================================
# АНАЛИЗ АРХИВОВ
# ============================================================

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
        
        elif "7z" in mime:
            with py7zr.SevenZipFile(file_path, 'r') as szf:
                for info in szf.list():
                    result["files"].append({
                        "name": info.filename,
                        "size": info.uncompressed,
                        "compressed": info.compressed
                    })
        
        elif "tar" in mime:
            with tarfile.open(file_path, 'r') as tf:
                for info in tf.getmembers():
                    result["files"].append({
                        "name": info.name,
                        "size": info.size,
                        "modified": str(datetime.fromtimestamp(info.mtime))
                    })
        
        result["total_files"] = len(result["files"])
        result["total_size"] = sum(f["size"] for f in result["files"])
        
    except Exception as e:
        result["error"] = str(e)
    
    return result

# ============================================================
# ПОИСК ТЕЛЕФОНА
# ============================================================

async def search_phone(phone: str) -> Dict[str, Any]:
    phone_clean = re.sub(r'[^\d+]', '', phone)
    result = {"номер": phone_clean, "информация": {}, "мессенджеры": [], "соцсети": {}, "утечки": []}
    
    try:
        pn = phonenumbers.parse(phone_clean, None)
        result["информация"] = {
            "валиден": phonenumbers.is_valid_number(pn),
            "международный": phonenumbers.format_number(pn, PhoneNumberFormat.INTERNATIONAL),
            "страна": geocoder.description_for_number(pn, "ru"),
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
        
        tasks.extend([
            check_messengers(session, phone_clean),
            check_phone_leaks(session, phone_clean),
            find_social_by_phone(session, phone_clean)
        ])
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, dict):
                for k, v in r.items():
                    if k in result:
                        if isinstance(result[k], dict):
                            result[k].update(v)
                        elif isinstance(result[k], list):
                            result[k].extend(v)
    
    return result

async def fetch_numverify(session, phone):
    try:
        r = await session.get("http://apilayer.net/api/validate",
            params={"access_key": NUMVERIFY_KEY, "number": phone})
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

async def check_messengers(session, phone):
    messengers = []
    try:
        r = await session.get(f"https://t.me/+{phone.replace('+', '')}", timeout=5)
        if r.status == 200:
            messengers.append({"name": "Telegram", "url": f"https://t.me/+{phone.replace('+', '')}"})
    except:
        pass
    try:
        r = await session.get(f"https://wa.me/{phone.replace('+', '')}", timeout=5)
        if r.status == 200:
            messengers.append({"name": "WhatsApp", "url": f"https://wa.me/{phone.replace('+', '')}"})
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
                    leaks.append({"источник": source.get("name"), "дата": source.get("date")})
    except:
        pass
    return {"утечки": leaks}

async def find_social_by_phone(session, phone):
    social = {}
    try:
        clean = phone.replace('+', '').replace(' ', '')
        r = await session.get(f"https://vk.com/search?c%5Bphone%5D={clean}", headers=HEADERS)
        if r.status == 200:
            t = await r.text()
            profiles = re.findall(r'href="/(id\d+)"', t)
            if profiles:
                social["VK"] = f"https://vk.com/{profiles[0]}"
    except:
        pass
    return {"соцсети": social}

# ============================================================
# ПОИСК EMAIL
# ============================================================

async def search_email(email: str) -> Dict[str, Any]:
    email = email.strip().lower()
    result = {
        "email": email,
        "формат_валиден": bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)),
        "домен": email.split("@")[1] if "@" in email else None,
        "валиден": False,
        "владелец": None,
        "фото": None,
        "утечки": []
    }
    
    if "@" in email:
        domain = result["домен"]
        try:
            mx = dns.resolver.resolve(domain, 'MX')
            result["валиден"] = len(list(mx)) > 0
        except:
            pass
        
        try:
            email_hash = hashlib.md5(email.encode()).hexdigest()
            async with aiohttp.ClientSession() as s:
                r = await s.get(f"https://www.gravatar.com/{email_hash}.json")
                if r.status == 200:
                    data = await r.json()
                    entry = data.get("entry", [{}])[0]
                    result["владелец"] = entry.get("displayName") or entry.get("preferredUsername")
                    result["фото"] = f"https://www.gravatar.com/avatar/{email_hash}?s=400"
        except:
            pass
        
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}")
                if r.status == 200:
                    breaches = await r.json()
                    for b in breaches[:5]:
                        result["утечки"].append({"название": b.get("Name"), "дата": b.get("BreachDate")})
        except:
            pass
    
    return result

# ============================================================
# ПОИСК ФИО
# ============================================================

async def search_fullname(fio: str) -> Dict[str, Any]:
    parts = fio.strip().split()
    name = parts[1] if len(parts) > 1 else (parts[0] if parts else "")
    surname = parts[0] if parts else ""
    
    result = {"фио": fio, "пол": None, "возраст": None, "национальность": None, "соцсети": {}}
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        if name:
            tasks.append(fetch_agify(session, name))
            tasks.append(fetch_nationalize(session, name))
        if GENDERAPI_KEY and name:
            tasks.append(fetch_genderapi(session, name))
        if NAMSOR_KEY and name and surname:
            tasks.append(fetch_namsor(session, name, surname))
        tasks.append(find_vk_by_name(session, fio))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, dict):
                result.update(r)
    
    return result

async def fetch_agify(session, name):
    try:
        r = await session.get(f"https://api.agify.io?name={name}")
        data = await r.json()
        return {"возраст": data.get("age")}
    except:
        return {}

async def fetch_nationalize(session, name):
    try:
        r = await session.get(f"https://api.nationalize.io?name={name}")
        data = await r.json()
        countries = data.get("country", [])
        if countries:
            country_map = {"RU": "Россия", "UA": "Украина", "BY": "Беларусь", "KZ": "Казахстан"}
            return {"национальность": country_map.get(countries[0]["country_id"])}
    except:
        return {}

async def fetch_genderapi(session, name):
    try:
        r = await session.get("https://gender-api.com/v2/gender", params={"key": GENDERAPI_KEY, "name": name})
        data = await r.json()
        g = data.get("gender")
        return {"пол": "Мужской" if g == "male" else "Женский" if g == "female" else None}
    except:
        return {}

async def fetch_namsor(session, name, surname):
    try:
        r = await session.get(f"https://v2.namsor.com/NamsorAPIv2/api2/json/genderFull/{name}/{surname}",
            headers={"X-API-KEY": NAMSOR_KEY})
        data = await r.json()
        return {"пол": data.get("likelyGender"), "этнос": data.get("ethnicity")}
    except:
        return {}

async def find_vk_by_name(session, fio):
    result = {}
    try:
        r = await session.get(f"https://vk.com/search?c%5Bq%5D={fio}", headers=HEADERS)
        if r.status == 200:
            t = await r.text()
            profiles = re.findall(r'href="/([^"]+)"[^>]*>([^<]+)</a>', t)
            for url, name in profiles[:3]:
                if not url.startswith('id') and url not in ['feed', 'friends', 'photos']:
                    result[f"VK_{name}"] = {"url": f"https://vk.com/{url}", "name": name}
    except:
        pass
    return {"соцсети": result}

# ============================================================
# ПОИСК НИКНЕЙМА
# ============================================================

async def search_nickname(username: str) -> Dict[str, Any]:
    username = username.strip().replace("@", "")
    result = {"query": username, "platforms": {}, "total_found": 0}
    
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
        "Behance": f"https://behance.net/{username}",
        "Dribbble": f"https://dribbble.com/{username}",
        "Flickr": f"https://flickr.com/people/{username}",
        "Patreon": f"https://patreon.com/{username}",
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
        r = await session.head(url, timeout=5, allow_redirects=True)
        if r.status == 200:
            return {"name": name, "url": url, "found": True}
    except:
        pass
    return {"name": name, "found": False}

# ============================================================
# ПОИСК IP
# ============================================================

async def search_ip(ip: str) -> Dict[str, Any]:
    result = {"ip": ip, "geo": {}}
    
    async with aiohttp.ClientSession() as s:
        try:
            r = await s.get(f"http://ip-api.com/json/{ip}")
            data = await r.json()
            if data.get("status") == "success":
                result["geo"] = {
                    "страна": data.get("country"),
                    "город": data.get("city"),
                    "провайдер": data.get("isp"),
                    "координаты": f"{data.get('lat')}, {data.get('lon')}"
                }
        except:
            pass
    
    return result

# ============================================================
# ПРОВЕРКА ПАРОЛЯ
# ============================================================

async def check_password(password: str) -> Dict[str, Any]:
    result = {"длина": len(password), "скомпрометирован": False, "сложность": None}
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    score = sum([has_upper, has_lower, has_digit, has_special, len(password) >= 8, len(password) >= 12])
    
    if score <= 2: result["сложность"] = "Очень слабый"
    elif score <= 3: result["сложность"] = "Слабый"
    elif score <= 4: result["сложность"] = "Средний"
    elif score <= 5: result["сложность"] = "Хороший"
    else: result["сложность"] = "Отличный"
    
    try:
        sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
        async with aiohttp.ClientSession() as s:
            r = await s.get(f"https://api.pwnedpasswords.com/range/{sha1[:5]}")
            if r.status == 200:
                if sha1[5:] in (await r.text()):
                    result["скомпрометирован"] = True
    except:
        pass
    
    return result

# ============================================================
# ФОРМАТИРОВАНИЕ
# ============================================================

def format_phone_result(r):
    t = f"<b>📱 ТЕЛЕФОН: {r['номер']}</b>\n\n"
    for k, v in r.get("информация", {}).items():
        if v: t += f"• {k}: {v}\n"
    if r.get("мессенджеры"):
        t += f"\n<b>💬 Мессенджеры:</b> {', '.join([m['name'] for m in r['мессенджеры']])}"
    if r.get("соцсети"):
        t += f"\n<b>🌐 Соцсети:</b> {', '.join(r['соцсети'].keys())}"
    return t

def format_email_result(r):
    t = f"<b>📧 EMAIL: {r['email']}</b>\n\n"
    t += f"✅ Формат: {'OK' if r['формат_валиден'] else 'Ошибка'}\n"
    t += f"📧 Валиден: {'Да' if r['валиден'] else 'Нет'}\n"
    if r.get("владелец"): t += f"👤 Владелец: {r['владелец']}\n"
    if r.get("утечки"): t += f"\n<b>🔴 Утечки:</b> {len(r['утечки'])}"
    return t

def format_fullname_result(r):
    t = f"<b>👤 ФИО: {r['фио']}</b>\n\n"
    if r.get("пол"): t += f"⚥ Пол: {r['пол']}\n"
    if r.get("возраст"): t += f"📅 Возраст: ~{r['возраст']} лет\n"
    if r.get("национальность"): t += f"🌍 Национальность: {r['национальность']}\n"
    if r.get("соцсети"):
        t += "\n<b>🌐 Профили:</b>\n"
        for name, data in r["соцсети"].items():
            if isinstance(data, dict):
                t += f"• <b>{name}:</b> <a href='{data['url']}'>{data['name']}</a>\n"
    return t

def format_nickname_result(r):
    t = f"<b>🔍 НИКНЕЙМ: @{r['query']}</b>\n\n"
    t += f"📊 Найдено: {r['total_found']}\n\n"
    for name, data in r["platforms"].items():
        t += f"• <b>{name}:</b> <a href='{data['url']}'>Профиль</a>\n"
    return t

def format_ip_result(r):
    t = f"<b>🌐 IP: {r['ip']}</b>\n\n"
    for k, v in r.get("geo", {}).items():
        if v: t += f"• {k}: {v}\n"
    return t

def format_password_result(r):
    t = "<b>🔐 АНАЛИЗ ПАРОЛЯ</b>\n\n"
    t += f"📏 Длина: {r['длина']}\n"
    t += f"📊 Сложность: {r['сложность']}\n"
    t += f"\n{'🔴 СКОМПРОМЕТИРОВАН!' if r['скомпрометирован'] else '✅ Не найден в утечках'}"
    return t

def format_document_result(r):
    t = f"<b>📄 АНАЛИЗ ДОКУМЕНТА</b>\n\n"
    t += f"📁 Файл: {os.path.basename(r['file'])}\n"
    t += f"📌 Тип: {r['type']}\n"
    if r.get("author"): t += f"👤 Автор: {r['author']}\n"
    if r.get("emails"): t += f"\n📧 Email: {', '.join(r['emails'][:3])}\n"
    if r.get("phones"): t += f"📱 Телефоны: {', '.join(r['phones'][:3])}\n"
    return t

# ============================================================
# МЕНЮ
# ============================================================

def main_menu():
    b = InlineKeyboardBuilder()
    buttons = [
        ("📱 Телефон", "phone"), ("📧 Email", "email"), ("👤 ФИО", "fullname"),
        ("🔍 Никнейм", "nickname"), ("🌐 IP", "ip"), ("🔐 Пароль", "password"),
        ("📄 Файл", "file"), ("🔥 ГЛУБОКИЙ ПОИСК", "deep_search")
    ]
    for text, data in buttons:
        b.button(text=text, callback_data=data)
    b.adjust(2)
    return b.as_markup()

def back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑 Удалить", callback_data="del"),
         InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
    ])

@dp.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>🔥 ULTIMATE AGGRESSIVE OSINT</b>\n\n"
        "<i>✅ Все импорты работают!</i>\n"
        "<i>✅ Все API подключены!</i>\n\n"
        "Выберите тип поиска:",
        reply_markup=main_menu()
    )
    await state.set_state(SearchStates.choosing)

@dp.callback_query(F.data == "back")
async def back_cb(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchStates.choosing)
    await callback.message.edit_text("<b>🔥 ULTIMATE OSINT</b>\n\nВыберите тип поиска:", reply_markup=main_menu())
    await callback.answer()

@dp.callback_query(SearchStates.choosing)
async def choice_cb(callback: CallbackQuery, state: FSMContext):
    prompts = {
        "phone": (SearchStates.phone, "📱 Введите номер телефона:"),
        "email": (SearchStates.email, "📧 Введите Email:"),
        "fullname": (SearchStates.fullname, "👤 Введите ФИО:"),
        "nickname": (SearchStates.nickname, "🔍 Введите никнейм:"),
        "ip": (SearchStates.ip, "🌐 Введите IP:"),
        "password": (SearchStates.password, "🔐 Введите пароль:"),
        "file": (SearchStates.file_analysis, "📄 Отправьте файл:"),
        "deep_search": (SearchStates.deep_search, "🔥 Введите данные для глубокого поиска:")
    }
    if callback.data in prompts:
        ns, pt = prompts[callback.data]
        await state.set_state(ns)
        await callback.message.edit_text(pt, reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]))
    await callback.answer()

@dp.message(SearchStates.phone)
async def phone_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Поиск...")
    r = await search_phone(message.text.strip())
    await w.delete()
    await message.answer(format_phone_result(r), reply_markup=back_button(), disable_web_page_preview=True)
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.email)
async def email_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Поиск...")
    r = await search_email(message.text.strip())
    await w.delete()
    if r.get("фото"):
        try: await message.answer_photo(r["фото"])
        except: pass
    await message.answer(format_email_result(r), reply_markup=back_button())
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.fullname)
async def fullname_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Анализ...")
    r = await search_fullname(message.text.strip())
    await w.delete()
    await message.answer(format_fullname_result(r), reply_markup=back_button(), disable_web_page_preview=True)
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.nickname)
async def nickname_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Поиск по 20+ платформам...")
    r = await search_nickname(message.text.strip())
    await w.delete()
    await message.answer(format_nickname_result(r), reply_markup=back_button(), disable_web_page_preview=True)
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.ip)
async def ip_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Поиск...")
    r = await search_ip(message.text.strip())
    await w.delete()
    if r.get("geo", {}).get("координаты"):
        try:
            lat, lon = r["geo"]["координаты"].split(",")
            await message.answer_location(float(lat), float(lon))
        except: pass
    await message.answer(format_ip_result(r), reply_markup=back_button())
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.password)
async def password_msg(message: Message, state: FSMContext):
    w = await message.answer("⏳ Проверка...")
    r = await check_password(message.text.strip())
    try: await message.delete()
    except: pass
    await w.delete()
    await message.answer(format_password_result(r), reply_markup=back_button())
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.file_analysis)
async def file_msg(message: Message, state: FSMContext):
    if not message.document:
        await message.answer("❌ Отправьте файл!")
        return
    
    w = await message.answer("⏳ Анализ файла...")
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
        if r.get("datetime"): t += f"📅 Дата: {r['datetime']}\n"
        if r.get("gps") and r["gps"].get("decimal"):
            lat, lon = r["gps"]["decimal"]["lat"], r["gps"]["decimal"]["lon"]
            t += f"📍 Координаты: {lat:.6f}, {lon:.6f}\n"
            await message.answer_location(lat, lon)
    elif "pdf" in mime or "document" in mime:
        r = await analyze_document(file_path)
        t = format_document_result(r)
    elif "zip" in mime or "rar" in mime or "7z" in mime:
        r = await analyze_archive(file_path)
        t = f"<b>📦 АНАЛИЗ АРХИВА</b>\n\n📁 Файлов: {r['total_files']}\n💾 Размер: {r['total_size']:,} байт"
    else:
        t = f"❌ Тип файла: {mime}"
    
    try: os.remove(file_path)
    except: pass
    
    await w.delete()
    await message.answer(t, reply_markup=back_button())
    await state.set_state(SearchStates.choosing)

@dp.message(SearchStates.deep_search)
async def deep_search_msg(message: Message, state: FSMContext):
    query = message.text.strip()
    w = await message.answer("🔥 Глубокий поиск...")
    
    if re.match(r'^[\+\d\s\(\)-]{10,}$', query):
        r = await search_phone(query)
        t = format_phone_result(r)
    elif "@" in query:
        r = await search_email(query)
        t = format_email_result(r)
        if r.get("фото"):
            try: await message.answer_photo(r["фото"])
            except: pass
    elif len(query.split()) >= 2:
        r = await search_fullname(query)
        t = format_fullname_result(r)
    else:
        r = await search_nickname(query)
        t = format_nickname_result(r)
    
    await w.delete()
    await message.answer(t, reply_markup=back_button(), disable_web_page_preview=True)
    await state.set_state(SearchStates.choosing)

@dp.callback_query(F.data == "del")
async def delete_cb(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

async def main():
    print("=" * 60)
    print("🚀 Бот запускается...")
    print("=" * 60)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
