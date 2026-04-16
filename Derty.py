import asyncio
import logging
import re
from datetime import datetime
from typing import Dict, Optional
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

storage = RedisStorage.from_url("redis://localhost:6379/3")
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)

logging.basicConfig(level=logging.INFO)

PHONE_APIS = {
    "numverify": {"key": os.getenv("NUMVERIFY_KEY", ""), "url": "http://apilayer.net/api/validate", "limit": 250, "priority": 1, "used": 0},
    "abstract": {"key": os.getenv("ABSTRACT_API_KEY", ""), "url": "https://phonevalidation.abstractapi.com/v1/", "limit": 100, "priority": 2, "used": 0},
    "veriphone": {"key": os.getenv("VERIPHONE_KEY", ""), "url": "https://api.veriphone.io/v2/verify", "limit": 100, "priority": 3, "used": 0}
}

EMAIL_APIS = {
    "zerobounce": {"key": os.getenv("ZEROBOUNCE_KEY", ""), "url": "https://api.zerobounce.net/v2/validate", "limit": 100, "priority": 1, "used": 0},
    "verifalia": {"key": os.getenv("VERIFALIA_KEY", ""), "url": "https://api.verifalia.com/v2.6/email-validations", "limit": 25, "priority": 2, "used": 0}
}

FULLNAME_APIS = {
    "nameapi": {"key": os.getenv("NAMEAPI_KEY", ""), "url": "https://api.nameapi.org/rest/v5.3/parser/person-name-parser", "limit": 1000, "priority": 1, "used": 0},
    "namsor": {"key": os.getenv("NAMSOR_KEY", ""), "url": "https://v2.namsor.com/NamsorAPIv2/api2/json/genderFull", "limit": 1000, "priority": 2, "used": 0},
    "genderapi": {"key": os.getenv("GENDERAPI_KEY", ""), "url": "https://gender-api.com/v2/gender", "limit": 500, "priority": 3, "used": 0}
}

ADDRESS_APIS = {
    "geoapify": {"key": os.getenv("GEOAPIFY_KEY", ""), "url": "https://api.geoapify.com/v1/geocode/search", "limit": 3000, "priority": 1, "used": 0},
    "positionstack": {"key": os.getenv("POSITIONSTACK_KEY", ""), "url": "http://api.positionstack.com/v1/forward", "limit": 25000, "priority": 2, "used": 0}
}

TELEGRAM_APIS = {
    "telemetr": {"key": os.getenv("TELEMETR_KEY", ""), "url": "https://api.telemetr.io/v1/channel", "limit": 100, "priority": 1, "used": 0},
    "tgstat": {"key": os.getenv("TGSTAT_KEY", ""), "url": "https://api.tgstat.ru/channels/search", "limit": 50, "priority": 2, "used": 0},
    "tgscan": {"key": os.getenv("TGSCAN_KEY", ""), "url": "https://api.tgscan.io/v1/search", "limit": 100, "priority": 3, "used": 0},
    "combot": {"key": os.getenv("COMBOT_KEY", ""), "url": "https://api.combot.io/v1/channel", "limit": 300, "priority": 4, "used": 0}
}

IP_APIS = {
    "ipinfo": {"key": os.getenv("IPINFO_KEY", ""), "url": "https://ipinfo.io", "limit": 50000, "priority": 1, "used": 0},
    "ipgeolocation": {"key": os.getenv("IPGEOLOCATION_KEY", ""), "url": "https://api.ipgeolocation.io/ipgeo", "limit": 1000, "priority": 2, "used": 0}
}

class SearchStates(StatesGroup):
    choosing_segment = State()
    entering_phone = State()
    entering_email = State()
    entering_fullname = State()
    entering_address = State()
    entering_vk = State()
    entering_tg = State()
    entering_ip = State()

class APIManager:
    def __init__(self, config): self.config = config; self.usage = {n: 0 for n in config}
    def get_available(self):
        a = [(n, c["priority"]) for n, c in self.config.items() if c.get("key") and self.usage[n] < c["limit"]]
        return sorted(a, key=lambda x: x[1])[0][0] if a else None
    def increment(self, n):
        if n in self.usage: self.usage[n] += 1

phone_mgr = APIManager(PHONE_APIS)
email_mgr = APIManager(EMAIL_APIS)
fullname_mgr = APIManager(FULLNAME_APIS)
address_mgr = APIManager(ADDRESS_APIS)
telegram_mgr = APIManager(TELEGRAM_APIS)
ip_mgr = APIManager(IP_APIS)

async def search_phone_numverify(p, k):
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(PHONE_APIS["numverify"]["url"], params={"access_key": k, "number": p})).json()
            return {"valid": r.get("valid"), "country": r.get("country_name"), "location": r.get("location"), "carrier": r.get("carrier"), "type": r.get("line_type")}
        except: return {"error": "err"}

async def search_phone_abstract(p, k):
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(PHONE_APIS["abstract"]["url"], params={"api_key": k, "phone": p})).json()
            return {"valid": r.get("valid"), "country": r.get("country", {}).get("name"), "carrier": r.get("carrier"), "type": r.get("line_type")}
        except: return {"error": "err"}

async def search_phone_veriphone(p, k):
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(PHONE_APIS["veriphone"]["url"], params={"key": k, "phone": p})).json()
            return {"valid": r.get("phone_valid"), "country": r.get("country"), "carrier": r.get("carrier")}
        except: return {"error": "err"}

async def search_phone(p):
    sel = phone_mgr.get_available()
    if not sel: return {"error": "limit"}
    f = {"numverify": lambda: search_phone_numverify(p, PHONE_APIS["numverify"]["key"]),
         "abstract": lambda: search_phone_abstract(p, PHONE_APIS["abstract"]["key"]),
         "veriphone": lambda: search_phone_veriphone(p, PHONE_APIS["veriphone"]["key"])}
    r = await f[sel]()
    phone_mgr.increment(sel)
    return r

async def search_email_zerobounce(e, k):
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(EMAIL_APIS["zerobounce"]["url"], params={"email": e, "api_key": k})).json()
            return {"valid": r.get("status") == "valid", "disposable": r.get("disposable") == "true", "first": r.get("firstname"), "last": r.get("lastname")}
        except: return {"error": "err"}

async def search_email_verifalia(e, k):
    async with aiohttp.ClientSession() as s:
        try:
            h = {"Authorization": f"Bearer {k}"}
            j = await (await s.post(EMAIL_APIS["verifalia"]["url"], json={"entries": [{"inputData": e}]}, headers=h)).json()
            if j.get("id"):
                await asyncio.sleep(2)
                r = await (await s.get(f"{EMAIL_APIS['verifalia']['url']}/{j['id']}", headers=h)).json()
                en = r.get("entries", [{}])[0]
                return {"valid": en.get("status") == "Success", "disposable": en.get("disposable") == "true"}
        except: return {"error": "err"}
    return {"error": "err"}

async def search_email(e):
    sel = email_mgr.get_available()
    if not sel: return {"error": "limit"}
    f = {"zerobounce": lambda: search_email_zerobounce(e, EMAIL_APIS["zerobounce"]["key"]),
         "verifalia": lambda: search_email_verifalia(e, EMAIL_APIS["verifalia"]["key"])}
    r = await f[sel]()
    email_mgr.increment(sel)
    return r

async def search_fullname_nameapi(fio, k):
    async with aiohttp.ClientSession() as s:
        try:
            d = {"inputPerson": {"name": {"nameFields": [{"stringValue": fio}]}}}
            r = await (await s.post(FULLNAME_APIS["nameapi"]["url"], params={"apiKey": k}, json=d)).json()
            m = r.get("matches", [{}])[0]
            return {"gender": m.get("gender", {}).get("gender")}
        except: return {"error": "err"}

async def search_fullname_namsor(fio, k):
    p = fio.split()
    fn, ln = p[0], p[-1] if len(p) > 1 else ""
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(f"{FULLNAME_APIS['namsor']['url']}/{fn}/{ln}", headers={"X-API-KEY": k})).json()
            return {"gender": r.get("likelyGender"), "ethnicity": r.get("ethnicity"), "country": r.get("countryOrigin")}
        except: return {"error": "err"}

async def search_fullname_genderapi(fio, k):
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(FULLNAME_APIS["genderapi"]["url"], params={"key": k, "name": fio.split()[0]})).json()
            return {"gender": r.get("gender"), "accuracy": r.get("accuracy")}
        except: return {"error": "err"}

async def search_fullname(fio):
    r = {}
    if FULLNAME_APIS["nameapi"]["key"]: r["nameapi"] = await search_fullname_nameapi(fio, FULLNAME_APIS["nameapi"]["key"])
    if FULLNAME_APIS["namsor"]["key"]: r["namsor"] = await search_fullname_namsor(fio, FULLNAME_APIS["namsor"]["key"])
    if FULLNAME_APIS["genderapi"]["key"]: r["genderapi"] = await search_fullname_genderapi(fio, FULLNAME_APIS["genderapi"]["key"])
    return r

async def search_address_geoapify(a, k):
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(ADDRESS_APIS["geoapify"]["url"], params={"text": a, "apiKey": k, "limit": 2})).json()
            f = r.get("features", [])
            return {"found": len(f), "results": [{"addr": x.get("properties", {}).get("formatted"), "lat": x.get("geometry", {}).get("coordinates", [])[1], "lon": x.get("geometry", {}).get("coordinates", [])[0]} for x in f[:2]]}
        except: return {"error": "err"}

async def search_address_positionstack(a, k):
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(ADDRESS_APIS["positionstack"]["url"], params={"access_key": k, "query": a, "limit": 2})).json()
            d = r.get("data", [])
            return {"found": len(d), "results": [{"addr": x.get("label"), "lat": x.get("latitude"), "lon": x.get("longitude")} for x in d[:2]]}
        except: return {"error": "err"}

async def search_address(a):
    r = {}
    if ADDRESS_APIS["geoapify"]["key"]: r["geo"] = await search_address_geoapify(a, ADDRESS_APIS["geoapify"]["key"])
    if ADDRESS_APIS["positionstack"]["key"]: r["pos"] = await search_address_positionstack(a, ADDRESS_APIS["positionstack"]["key"])
    return r

async def search_vk_public(u):
    u = u.strip().replace("https://vk.com/", "").replace("vk.com/", "")
    h = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession() as s:
        try:
            url = f"https://vk.com/id{u}" if u.isdigit() else f"https://vk.com/{u}"
            r = await s.get(url, headers=h, timeout=10)
            if r.status != 200: return {"exists": False}
            t = await r.text()
            if "Page not found" in t: return {"exists": False}
            nm = re.search(r'<title>([^<]+)</title>', t)
            im = re.search(r'<meta property="og:image" content="([^"]+)"', t)
            return {"exists": True, "name": nm.group(1) if nm else "", "avatar": im.group(1) if im else None, "url": url}
        except: return {"error": "err"}

async def search_vk_wall(u):
    u = u.strip().replace("https://vk.com/", "").replace("vk.com/", "")
    h = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession() as s:
        try:
            url = f"https://vk.com/wall{u}" if u.isdigit() else f"https://vk.com/{u}"
            r = await s.get(url, headers=h, timeout=10)
            if r.status != 200: return {"posts": []}
            t = await r.text()
            posts = re.findall(r'class="wall_post_text">([^<]+)<', t)
            return {"posts": [{"text": p[:150]} for p in posts[:5]]}
        except: return {"posts": []}

async def search_telegram_telemetr(u, k):
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(f"{TELEGRAM_APIS['telemetr']['url']}/{u}", params={"api_key": k})).json()
            return {"subs": r.get("subscribers"), "er": r.get("er")}
        except: return {"error": "err"}

async def search_telegram_tgstat(u, k):
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(TELEGRAM_APIS["tgstat"]["url"], params={"q": u, "token": k, "limit": 1})).json()
            i = r.get("response", {}).get("items", [])
            return {"subs": i[0].get("participants_count")} if i else {}
        except: return {"error": "err"}

async def search_telegram_combot(u, k):
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(f"{TELEGRAM_APIS['combot']['url']}/{u}", headers={"Authorization": f"Bearer {k}"})).json()
            return {"subs": r.get("subscribers"), "title": r.get("title")}
        except: return {"error": "err"}

async def search_telegram(u):
    r = {}
    if TELEGRAM_APIS["telemetr"]["key"]: r["tm"] = await search_telegram_telemetr(u, TELEGRAM_APIS["telemetr"]["key"])
    if TELEGRAM_APIS["tgstat"]["key"]: r["ts"] = await search_telegram_tgstat(u, TELEGRAM_APIS["tgstat"]["key"])
    if TELEGRAM_APIS["combot"]["key"]: r["cb"] = await search_telegram_combot(u, TELEGRAM_APIS["combot"]["key"])
    return r

async def search_ip_ipinfo(ip, k):
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(f"{IP_APIS['ipinfo']['url']}/{ip}", headers={"Authorization": f"Bearer {k}"})).json()
            return {"city": r.get("city"), "region": r.get("region"), "country": r.get("country"), "org": r.get("org")}
        except: return {"error": "err"}

async def search_ip_ipgeolocation(ip, k):
    async with aiohttp.ClientSession() as s:
        try:
            r = await (await s.get(IP_APIS["ipgeolocation"]["url"], params={"apiKey": k, "ip": ip})).json()
            return {"city": r.get("city"), "country": r.get("country_name"), "isp": r.get("isp"), "lat": r.get("latitude"), "lon": r.get("longitude")}
        except: return {"error": "err"}

async def search_ip(ip):
    r = {}
    if IP_APIS["ipinfo"]["key"]: r["info"] = await search_ip_ipinfo(ip, IP_APIS["ipinfo"]["key"])
    if IP_APIS["ipgeolocation"]["key"]: r["geo"] = await search_ip_ipgeolocation(ip, IP_APIS["ipgeolocation"]["key"])
    return r

def get_main_keyboard():
    b = InlineKeyboardBuilder()
    for t, d in [("📱", "phone"), ("📧", "email"), ("👤", "fullname"), ("🏠", "address"), ("📘", "vk"), ("✈️", "tg"), ("🌐", "ip")]:
        b.button(text=t, callback_data=d)
    b.adjust(3)
    return b.as_markup()

@dp.message(Command("start"))
async def start(m: Message, s: FSMContext):
    await s.clear()
    await m.answer("<b>VICTIM OSINT</b>", reply_markup=get_main_keyboard())
    await s.set_state(SearchStates.choosing_segment)

@dp.callback_query(SearchStates.choosing_segment)
async def choice(c: CallbackQuery, s: FSMContext):
    d = c.data
    prompts = {"phone": (SearchStates.entering_phone, "<b>📱 Номер</b>"), "email": (SearchStates.entering_email, "<b>📧 Email</b>"),
               "fullname": (SearchStates.entering_fullname, "<b>👤 ФИО</b>"), "address": (SearchStates.entering_address, "<b>🏠 Адрес</b>"),
               "vk": (SearchStates.entering_vk, "<b>📘 VK ID/ник</b>"), "tg": (SearchStates.entering_tg, "<b>✈️ Telegram @</b>"),
               "ip": (SearchStates.entering_ip, "<b>🌐 IP</b>")}
    if d in prompts:
        ns, pt = prompts[d]
        await s.set_state(ns)
        await c.message.edit_text(pt, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️", callback_data="back")]]))
    await c.answer()

@dp.callback_query(F.data == "back")
async def back(c: CallbackQuery, s: FSMContext):
    await s.set_state(SearchStates.choosing_segment)
    await c.message.edit_text("<b>VICTIM OSINT</b>", reply_markup=get_main_keyboard())
    await c.answer()

@dp.message(SearchStates.entering_phone)
async def phone(m: Message, s: FSMContext):
    w = await m.answer("...")
    r = await search_phone(m.text.strip())
    t = f"{'✅' if r.get('valid') else '❌'}\n{chr(10).join([f'{k}: {v}' for k,v in r.items() if v and k not in ['error','valid']])}"
    await w.delete()
    msg = await m.answer(t, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑", callback_data="del"), InlineKeyboardButton(text="◀️", callback_data="back")]]))
    asyncio.create_task(auto_delete(msg, 45))
    await s.set_state(SearchStates.choosing_segment)

@dp.message(SearchStates.entering_email)
async def email(m: Message, s: FSMContext):
    w = await m.answer("...")
    r = await search_email(m.text.strip())
    t = f"{'✅' if r.get('valid') else '❌'}"
    if r.get("first"): t += f"\n{r['first']} {r.get('last','')}"
    if r.get("disposable"): t += "\n⚠️"
    await w.delete()
    msg = await m.answer(t, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑", callback_data="del"), InlineKeyboardButton(text="◀️", callback_data="back")]]))
    asyncio.create_task(auto_delete(msg, 45))
    await s.set_state(SearchStates.choosing_segment)

@dp.message(SearchStates.entering_fullname)
async def fullname(m: Message, s: FSMContext):
    w = await m.answer("...")
    r = await search_fullname(m.text.strip())
    t = ""
    if "nameapi" in r and r["nameapi"].get("gender"): t += f"📝 {r['nameapi']['gender']}\n"
    if "namsor" in r and r["namsor"].get("gender"): t += f"🌍 {r['namsor']['gender']} ({r['namsor'].get('country','')})\n"
    if "genderapi" in r and r["genderapi"].get("gender"): t += f"⚥ {r['genderapi']['gender']} ({r['genderapi'].get('accuracy','')}%)"
    await w.delete()
    msg = await m.answer(t or "—", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑", callback_data="del"), InlineKeyboardButton(text="◀️", callback_data="back")]]))
    asyncio.create_task(auto_delete(msg, 45))
    await s.set_state(SearchStates.choosing_segment)

@dp.message(SearchStates.entering_address)
async def address(m: Message, s: FSMContext):
    w = await m.answer("...")
    r = await search_address(m.text.strip())
    t = ""
    for k, v in r.items():
        if v.get("found"):
            for x in v["results"][:1]:
                t += f"📍 {x['addr'][:50]}...\n"
                if x.get("lat"): await m.answer_location(float(x["lat"]), float(x["lon"]))
    await w.delete()
    msg = await m.answer(t or "—", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑", callback_data="del"), InlineKeyboardButton(text="◀️", callback_data="back")]]))
    asyncio.create_task(auto_delete(msg, 45))
    await s.set_state(SearchStates.choosing_segment)

@dp.message(SearchStates.entering_vk)
async def vk(m: Message, s: FSMContext):
    w = await m.answer("...")
    p = await search_vk_public(m.text.strip())
    wall = await search_vk_wall(m.text.strip())
    t = ""
    if p.get("exists"):
        t = f"✅ {p.get('name','')}"
        if p.get("avatar"): await m.answer_photo(p["avatar"])
    else:
        t = "❌"
    if wall.get("posts"):
        t += f"\n📝 {wall['posts'][0]['text']}" if wall["posts"] else ""
    await w.delete()
    msg = await m.answer(t or "—", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑", callback_data="del"), InlineKeyboardButton(text="◀️", callback_data="back")]]))
    asyncio.create_task(auto_delete(msg, 45))
    await s.set_state(SearchStates.choosing_segment)

@dp.message(SearchStates.entering_tg)
async def tg(m: Message, s: FSMContext):
    w = await m.answer("...")
    u = m.text.strip().replace("@", "")
    r = await search_telegram(u)
    t = ""
    if r.get("tm") and r["tm"].get("subs"): t += f"📊 {r['tm']['subs']}"
    if r.get("ts") and r["ts"].get("subs"): t += f"\n📈 {r['ts']['subs']}"
    if r.get("cb") and r["cb"].get("title"): t += f"\n🤖 {r['cb']['title']}"
    await w.delete()
    msg = await m.answer(t or "—", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑", callback_data="del"), InlineKeyboardButton(text="◀️", callback_data="back")]]))
    asyncio.create_task(auto_delete(msg, 45))
    await s.set_state(SearchStates.choosing_segment)

@dp.message(SearchStates.entering_ip)
async def ip(m: Message, s: FSMContext):
    w = await m.answer("...")
    r = await search_ip(m.text.strip())
    t = ""
    for k, v in r.items():
        if v.get("city"): t += f"📍 {v.get('city','')}, {v.get('country','')}\n"
        if v.get("org"): t += f"🏢 {v['org']}\n"
        if v.get("lat"): await m.answer_location(float(v["lat"]), float(v["lon"]))
    await w.delete()
    msg = await m.answer(t or "—", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗑", callback_data="del"), InlineKeyboardButton(text="◀️", callback_data="back")]]))
    asyncio.create_task(auto_delete(msg, 45))
    await s.set_state(SearchStates.choosing_segment)

async def auto_delete(msg, d):
    await asyncio.sleep(d)
    try: await msg.delete()
    except: pass

@dp.callback_query(F.data == "del")
async def delete(c: CallbackQuery):
    await c.message.delete()
    await c.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())