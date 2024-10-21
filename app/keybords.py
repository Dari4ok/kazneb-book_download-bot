from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

ziporpdf = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='zip',callback_data='zip'),
    InlineKeyboardButton(text='pdf',callback_data='pdf')]
    ])
