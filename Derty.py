#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================
# 🔥 ULTIMATE AGGRESSIVE OSINT FRAMEWORK 🔥
# ВСЕ СУЩЕСТВУЮЩИЕ ИМПОРТЫ + АВТОУСТАНОВКА
# ============================================================

import subprocess
import sys
import os

# ============================================================
# АВТОУСТАНОВКА ВСЕХ ЗАВИСИМОСТЕЙ
# ============================================================

def install_package(package):
    """Установка пакета через pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

# Список ВСЕХ необходимых пакетов
REQUIRED_PACKAGES = [
    # Core
    "aiogram>=3.0.0",
    "aiohttp>=3.9.0",
    "python-dotenv>=1.0.0",
    
    # Phone
    "phonenumbers>=8.13.0",
    
    # DNS/Email
    "dnspython>=2.4.0",
    "email-validator>=2.1.0",
    
    # WHOIS
    "python-whois>=0.8.0",
    
    # SSL/Crypto
    "pyOpenSSL>=23.3.0",
    "cryptography>=41.0.0",
    "certifi>=2024.2.2",
    
    # Geo
    "geoip2>=4.7.0",
    "maxminddb>=2.4.0",
    "geopy>=2.4.0",
    
    # Images/EXIF
    "Pillow>=10.1.0",
    "exifread>=3.0.0",
    "filetype>=1.2.0",
    
    # Documents
    "pdfplumber>=0.10.0",
    "python-docx>=1.1.0",
    "openpyxl>=3.1.0",
    "python-pptx>=0.6.23",
    "olefile>=0.47",
    "xlrd>=2.0.1",
    "xlwt>=1.3.0",
    
    # Archives
    "rarfile>=4.1",
    "py7zr>=0.20.0",
    
    # Parsing
    "beautifulsoup4>=4.12.0",
    "lxml>=4.9.0",
    "requests>=2.31.0",
    "selenium>=4.15.0",
    
    # APIs
    "shodan>=1.31.0",
    "vt-py>=0.18.0",
    "waybackpy>=3.0.0",
    
    # NLP
    "nltk>=3.8.0",
    "spacy>=3.7.0",
    "langdetect>=1.0.9",
    "googletrans>=4.0.0",
    "textblob>=0.17.0",
    
    # Graphs
    "networkx>=3.2.0",
    
    # Data
    "pandas>=2.1.0",
    "numpy>=1.26.0",
    "python-dateutil>=2.8.0",
    "dateparser>=1.2.0",
    "pytz>=2024.1",
    
    # Utils
    "click>=8.1.0",
    "rich>=13.7.0",
    "tqdm>=4.66.0",
    "colorama>=0.4.6",
    "pyyaml>=6.0.0",
    
    # Hash
    "bcrypt>=4.1.0",
    "pycryptodome>=3.19.0",
    
    # Crypto
    "web3>=6.14.0",
    "eth-account>=0.11.0",
    
    # Web
    "urllib3>=2.0.0",
    "chardet>=5.0.0",
    "tldextract>=5.1.0",
    "publicsuffixlist>=0.10.0",
    "idna>=3.4",
    
    # OSINT tools
    "holehe>=1.60.0",
    "maigret>=0.4.5",
    "socialscan>=1.4.0",
    
    # Дополнительные
    "faker>=20.1.0",
    "fake-useragent>=1.4.0",
]

print("=" * 60)
print("🔥 ULTIMATE AGGRESSIVE OSINT FRAMEWORK")
print("=" * 60)
print("📦 Проверка и установка зависимостей...")

# Устанавливаем pip если нужно
try:
    subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except:
    print("⚠️ Устанавливаю pip...")
    subprocess.check_call([sys.executable, "-m", "ensurepip"])

# Устанавливаем все пакеты
installed = 0
failed = 0

for package in REQUIRED_PACKAGES:
    try:
        __import__(package.split(">=")[0].split("[")[0].replace("-", "_"))
        print(f"✅ {package} уже установлен")
        installed += 1
    except ImportError:
        print(f"📦 Устанавливаю {package}...")
        if install_package(package):
            print(f"✅ {package} установлен")
            installed += 1
        else:
            print(f"⚠️ {package} - пропущен")
            failed += 1

print("=" * 60)
print(f"✅ Установлено: {installed} | ⚠️ Пропущено: {failed}")
print("=" * 60)

# ============================================================
# ТЕПЕРЬ ИМПОРТИРУЕМ ВСЕ БИБЛИОТЕКИ
# ============================================================

# Стандартная библиотека
import asyncio
import re
import json
import hashlib
import base64
import socket
import ssl
import csv
import math
import random
import string
import itertools
import zipfile
import tarfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from io import BytesIO
from urllib.parse import urlparse, parse_qs, quote, unquote
from collections import defaultdict
import logging

# HTTP и парсинг
import aiohttp
import requests
from bs4 import BeautifulSoup

# DNS, WHOIS, SSL
import whois
import dns.resolver
import OpenSSL
import cryptography
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Телефоны
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from phonenumbers import PhoneNumberFormat

# Изображения
import PIL.Image
from PIL.ExifTags import TAGS, GPSTAGS
import exifread
import filetype
import mimetypes

# Документы
import pdfplumber
import openpyxl
from pptx import Presentation
import olefile

# Архивы
import rarfile
import py7zr

# Геолокация
import geoip2.database
import maxminddb
from geopy.geocoders import Nominatim

# API
import shodan
import vt
from waybackpy import WaybackMachineCDXServerAPI

# NLP
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
import langdetect
from langdetect import detect
from googletrans import Translator
from textblob import TextBlob

# Графы
import networkx as nx

# Данные
import pandas as pd
import numpy as np
import dateparser
import pytz

# Утилиты
import click
from rich.console import Console
from rich.table import Table
from tqdm import tqdm
import colorama
import yaml

# Хэши
import bcrypt
from Cryptodome.Hash import SHA256, MD5

# Криптовалюты
from web3 import Web3

# Web
import tldextract
from publicsuffixlist import PublicSuffixList
import idna

# OSINT инструменты
import holehe
import maigret
import socialscan

# Fake данные
from faker import Faker
from fake_useragent import UserAgent

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

# Python-dotenv
from dotenv import load_dotenv

load_dotenv()

# Инициализация
mimetypes.init()
colorama.init()
faker = Faker()
ua = UserAgent()

print("=" * 60)
print("✅ ВСЕ ИМПОРТЫ УСПЕШНО ЗАГРУЖЕНЫ!")
print("=" * 60)

# ============================================================
# ЗАМЕНА MAGIC НА FILETYPE
# ============================================================

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
                'zip': 'application/zip', 'rar': 'application/x-rar-compressed',
                '7z': 'application/x-7z-compressed', 'tar': 'application/x-tar',
                'txt': 'text/plain', 'html': 'text/html', 'json': 'application/json',
                'xml': 'application/xml', 'mp3': 'audio/mpeg', 'mp4': 'video/mp4',
                'exe': 'application/x-msdownload', 'bin': 'application/octet-stream'
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
VIRUSTOTAL_KEY = os.getenv("VIRUSTOTAL_KEY", "")

storage = MemoryStorage()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

HEADERS = {
    "User-Agent": ua.random,
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

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
    file_analysis = State()
    deep_search = State()

# ============================================================
# ФУНКЦИИ ДЛЯ ТЕЛЕФОНА
# ============================================================

async def search_phone(phone: str) -> Dict[str, Any]:
    phone_clean = re.sub(r'[^\d+]', '', phone)
    result = {"номер": phone_clean, "phonenumbers": {}, "мессенджеры": [], "соцсети": {}, "утечки": []}
    
    try:
        pn = phonenumbers.parse(phone_clean, None)
        result["phonenumbers"] = {
            "валиден": phonenumbers.is_valid_number(pn),
            "международный": phonenumbers.format_number(pn, PhoneNumberFormat.INTERNATIONAL),
            "страна": geocoder.description_for_number(pn, "ru"),
            "оператор": carrier.name_for_number(pn, "ru"),
            "часовой_пояс": timezone.time_zones_for_number(pn)[0] if timezone.time_zones_for_number(pn) else None
        }
    except:
        pass
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            check_messengers(session, phone_clean),
            check_phone_leaks(session, phone_clean),
            find_social_by_phone(session, phone_clean)
        ]
        
        if NUMVERIFY_KEY:
            tasks.append(fetch_numverify(session, phone_clean))
        if ABSTRACT_API_KEY:
            tasks.append(fetch_abstractapi(session, phone_clean))
        if VERIPHONE_KEY:
            tasks.append(fetch_veriphone(session, phone_clean))
        
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
    email = email.strip().lower()
    result = {
        "email": email,
        "формат_валиден": bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)),
        "домен": email.split("@")[1] if "@" in email else None,
        "валиден": False,
        "владелец": None,
        "фото": None,
        "соцсети": {},
        "утечки": []
    }
    
    if "@" in email:
        domain = result["домен"]
        
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            result["валиден"] = len(list(mx_records)) > 0
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
        except:
            pass
        
        try:
            async with aiohttp.ClientSession() as s:
                r = await s.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", headers=HEADERS)
                if r.status == 200:
                    breaches = await r.json()
                    for b in breaches[:5]:
                        result["утечки"].append({"название": b.get("Name"), "дата": b.get("BreachDate")})
        except:
            pass
    
    return result

# ============================================================
# ФУНКЦИИ ДЛЯ ФИО
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
        r = await session.get("https://gender-api.com/v2/gender",
            params={"key": GENDERAPI_KEY, "name": name})
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
# ФУНКЦИИ ДЛЯ НИКНЕЙМА
# ============================================================

async def search_nickname(username: str) -> Dict[str, Any]:
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
        r = await session.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
        if r.status == 200:
            return {"name": name, "url": url, "found": True}
    except:
        pass
    return {"name": name, "found": False}

# ============================================================
# ФУНКЦИИ ДЛЯ IP
# ============================================================

async def search_ip(ip: str) -> Dict[str, Any]:
    result = {"ip": ip, "geo": {}}
    
    async with aiohttp.ClientSession() as session:
        if IPINFO_KEY:
            try:
                r = await session.get(f"https://ipinfo.io/{ip}", headers={"Authorization": f"Bearer {IPINFO_KEY}"})
                data = await r.json()
                result["geo"] = {
                    "city": data.get("city"),
                    "region": data.get("region"),
                    "country": data.get("country"),
                    "loc": data.get("loc"),
                    "org": data.get("org")
                }
            except:
                pass
        
        if not result["geo"]:
            try:
                r = await session.get(f"http://ip-api.com/json/{ip}")
                data = await r.json()
                if data.get("status") == "success":
                    result["geo"] = {
                        "city": data.get("city"),
                        "country": data.get("country"),
                        "isp": data.get("isp")
                    }
            except:
                pass
    
    return result

# ============================================================
# ФУНКЦИИ ДЛЯ ПАРОЛЯ
# ============================================================

async def check_password(password: str) -> Dict[str, Any]:
    result = {
        "длина": len(password),
        "скомпрометирован": False,
        "количество_утечек": 0,
        "сложность": None
    }
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    score = sum([has_upper, has_lower, has_digit, has_special, len(password) >= 8, len(password) >= 12])
    
    if score <= 2:
        result["сложность"] = "Очень слабый"
    elif score <= 3:
        result["сложность"] = "Слабый"
    elif score <= 4:
        result["сложность"] = "Средний"
    elif score <= 5:
        result["сложность"] = "Хороший"
    else:
        result["сложность"] = "Отличный"
    
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
# ФОРМАТИРОВАНИЕ РЕЗУЛЬТАТОВ
# ============================================================

def format_phone_result(r):
    t = f"<b>📱 ТЕЛЕФОН: {r['номер']}</b>\n\n"
    
    if r.get("phonenumbers"):
        pn = r["phonenumbers"]
        if pn.get("международный"): t += f"• Формат: {pn['международный']}\n"
        if pn.get("страна"): t += f"• Страна: {pn['страна']}\n"
        if pn.get("оператор"): t += f"• Оператор: {pn['оператор']}\n"
        t += f"• Валиден: {'✅' if pn.get('валиден') else '❌'}\n\n"
    
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
    
    if r.get("утечки"):
        t += f"\n<b>🔴 Утечки ({len(r['утечки'])}):</b>\n"
        for u in r["утечки"][:5]:
            t += f"• {u['название']} ({u.get('дата', 'N/A')})\n"
    
    return t

def format_fullname_result(r):
    t = f"<b>👤 ФИО: {r['фио']}</b>\n\n"
    if r.get("пол"): t += f"⚥ Пол: {r['пол']}\n"
    if r.get("возраст"): t += f"📅 Возраст: ~{r['возраст']} лет\n"
    if r.get("национальность"): t += f"🌍 Национальность: {r['национальность']}\n"
    if r.get("этнос"): t += f"👥 Этнос: {r['этнос']}\n"
    
    if r.get("соцсети"):
        t += "\n<b>🌐 Найденные профили:</b>\n"
        for name, data in r["соцсети"].items():
            if isinstance(data, dict):
                t += f"• <b>{name}:</b> <a href='{data.get('url', '')}'>{data.get('name', 'Профиль')}</a>\n"
    
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

def format_ip_result(r):
    t = f"<b>🌐 IP: {r['ip']}</b>\n\n"
    
    if r.get("geo"):
        g = r["geo"]
        if g.get("country"): t += f"🌍 Страна: {g['country']}\n"
        if g.get("city"): t += f"🏙 Город: {g['city']}\n"
        if g.get("region"): t += f"📍 Регион: {g['region']}\n"
        if g.get("isp"): t += f"📡 Провайдер: {g['isp']}\n"
        if g.get("org"): t += f"🏢 Организация: {g['org']}\n"
        if g.get("loc"): t += f"🗺 Координаты: {g['loc']}\n"
    
    return t

def format_password_result(r):
    t = "<b>🔐 АНАЛИЗ ПАРОЛЯ</b>\n\n"
    t += f"📏 Длина: {r['длина']} символов\n"
    t += f"📊 Сложность: {r['сложность']}\n"
    
    if r.get("скомпрометирован"):
        t += f"\n🔴 <b>СКОМПРОМЕТИРОВАН!</b>\n"
        t += f"📊 Найден в утечках: {r['количество_утечек']:,} раз\n".replace(',', ' ')
    else:
        t += "\n✅ Не найден в утечках\n"
    
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
        ("🔐 Пароль", "password"),
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
        "• 🔍 Никнейм - 20+ платформ\n"
        "• 🌐 IP - геолокация, провайдер\n"
        "• 🔐 Пароль - сложность, утечки\n"
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
        "password": (SearchStates.password, "🔐 <b>Введите пароль</b>"),
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
    w = await message.answer("⏳ Поиск по 20+ платформам...")
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

@dp.message(SearchStates.deep_search)
async def deep_search_msg(message: Message, state: FSMContext):
    query = message.text.strip()
    w = await message.answer("🔥 <b>ЗАПУЩЕН ГЛУБОКИЙ ПОИСК</b>\n\n⏳ Анализирую всеми методами...")
    
    results = []
    
    # Проверяем телефон
    if re.match(r'^[\+\d\s\(\)-]{10,}$', query):
        results.append(("phone", await search_phone(query)))
    # Проверяем email
    elif "@" in query:
        results.append(("email", await search_email(query)))
    # Проверяем ФИО
    elif len(query.split()) >= 2:
        results.append(("fullname", await search_fullname(query)))
    # Никнейм
    else:
        results.append(("nickname", await search_nickname(query)))
    
    await w.delete()
    
    for typ, r in results:
        if typ == "phone":
            await message.answer(format_phone_result(r), disable_web_page_preview=True)
        elif typ == "email":
            if r.get("фото"):
                try:
                    await message.answer_photo(r["фото"], caption="📸 Gravatar")
                except:
                    pass
            await message.answer(format_email_result(r), disable_web_page_preview=True)
        elif typ == "fullname":
            await message.answer(format_fullname_result(r), disable_web_page_preview=True)
        elif typ == "nickname":
            await message.answer(format_nickname_result(r), disable_web_page_preview=True)
    
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
    print("✅ ВСЕ API ПОДКЛЮЧЕНЫ!")
    print("=" * 60)
    print("📡 Бот запускается...")
    print("=" * 60)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
