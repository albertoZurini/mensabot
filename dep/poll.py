from urllib.request import urlopen
from bs4 import BeautifulSoup

from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext

DEBUG_ID = ""
CHAT_ID = [""]

updater = Updater(token='', use_context=True)

def add_emoticon(text):
    if "Sweets" in text:
        return f"{text}🧁🧁"
    return text

#dispatcher = updater.dispatcher
try:
    API_URL = "https://catering.dussmann.com/infineon-villach/speiseplaene/"
    html = urlopen(API_URL).read()
    soup = BeautifulSoup(html, features="html.parser")

    menu1_selector = "div.singleDay:nth-child(1) > div:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)"
    menu2_selector = "div.singleDay:nth-child(1) > div:nth-child(5) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)"
    night_selector = "div.singleDay:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)"
    fastlane_selector = "div.dishWrapper:nth-child(7) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)"
    grill_selector = "#c1365 > div > div:nth-child(1) > div:nth-child(7) > div.dish.clearfix > div.description > div.language02"
    vitalgericht_selector = "#c1365 > div > div:nth-child(1) > div:nth-child(8) > div.dish.clearfix > div.description > div.language02"

    selectors = [
        {
            "name": "MENU1",
            "selector": menu1_selector
        },
        {
            "name": "MENU2",
            "selector": menu2_selector
        },
        {
            "name": "GRILL",
            "selector": grill_selector
        },
        {
            "name": "VITALGERICHT",
            "selector": vitalgericht_selector
        },
        {
            "name": "FASTLANE",
            "selector": fastlane_selector
        },
        {
            "name": "NIGHT",
            "selector": night_selector
        }     
    ]

    # other endpoint has:
    """
    tr.tableColor:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(2)
    tr.tableColor:nth-child(2) > td:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(2)
    tr.tableColor:nth-child(2) > td:nth-child(4) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(2)
    """

    menu_info = ""

    for sel in selectors:
        text = ""
        try:
            text = soup.select_one(sel["selector"]).get_text().strip()
            text = add_emoticon(text)
        except Exception as e:
            text = f"Not available ({str(e)})"
        name = sel["name"]

        menu_info += f"{name}:\n\n{text}\n\n"

    for id in CHAT_ID:
        updater.bot.sendMessage(chat_id=id, text=menu_info)
except Exception as e:
    updater.bot.sendMessage(chat_id=DEBUG_ID, text=str(e))