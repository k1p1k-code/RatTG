from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def main_menu(data: dict):
    inline_keyboard = []
    for i in data:
        inline_keyboard.append([InlineKeyboardButton(
            text=i['name_short'], 
            callback_data=f'main_control_main_{i["uuid"]}'
        )])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)