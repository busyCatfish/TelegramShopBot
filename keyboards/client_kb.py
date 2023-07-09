from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from keys_token import tokens

b1 = KeyboardButton('Menu',web_app=WebAppInfo(url=tokens.app_url()))
#b2 = KeyboardButton('/Location')
#b3 = KeyboardButton('/Menu')
#b4 = KeyboardButton('Share contact',request_contact=True)
#b5 = KeyboardButton('Send loc', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1)#.add(b2).add(b3).row(b4,b5)