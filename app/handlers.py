from aiogram import F, Router
from aiogram.filters import CommandStart, command
from aiogram.types import Message, CallbackQuery
from app.pagedownloader import PageDownloader as pages

import app.keybords as kb

router = Router()
waiter = False
name = ''
link = 'link'
cash = ''
format = ''

@router.message(CommandStart())
async def com_start(message: Message):
    await message.reply('Cәлем, бұл бот kazneb сайтынан кітаптарды жүктеуге көмек береді. Бар болғаны кітапқа сілтеме жіберіңіз.')

@router.message(F.text.contains('kazneb.kz/kk/bookView'))
async def get_link(message: Message):
    global waiter
    global link
    await message.answer('Кітаптың аты қалай?')
    waiter = True
    link = message.text[0:-5]+'false'

@router.message(F.text)
async def get_name(message: Message):
    global name
    global waiter
    if waiter:
        waiter = False
        name = message.text
        await message.answer('Қай форматта ыңғайлы?', reply_markup=kb.ziporpdf)

@router.callback_query(F.data == 'zip')
async def zip(callback: CallbackQuery):
    global format
    global link
    global name

    format = 'zip'
    await callback.answer('Кітап zip форматта жүктеледі.')
    await callback.message.edit_text('Кітапты жүктеудеміз, күте тұрыңыз.')
    downloader = pages(link, name)
    downloader.download_pages()

@router.callback_query(F.data == 'pdf')
async def pdf(callback: CallbackQuery):
    global format
    format = 'pdf'
    await callback.answer('Кітап pdf форматта жүктеледі.')
    await callback.message.edit_text('Кітапты жүктеудеміз, күте тұрыңыз.')

