from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InputFile, callback_query, CallbackQuery

from app.pagedownloader import PageDownloader as pages
from app.image2pdf import PDFMaker
from os import removedirs, remove

import app.keybords as kb
import os


router = Router()
waiter = False
name = ''
link = 'link'

@router.callback_query(F.data == 'pdf')
async def zip_com(callback_query: CallbackQuery):
    await callback_query.answer('PDF формат жүктелуде')
    await callback_query.message.answer('Күте тұрыңыз, файл жүктелуде...')
    global link
    global name

    downloader = pages(link, name)
    downloader.download_pages()
    pdf_maker = PDFMaker(name) 
    pdf_maker.create_pdf()

    with open(f'{name}.pdf', 'rb') as file:
        pdf_file = InputFile(file, filename=f'{name}.pdf')

    if os.path.exists(f'{name}.pdf'):
        await callback_query.message.answer_document(document=pdf_file)
    else:
        await callback_query.message.answer("Кішігірм қателіктер, қайта көріңіз.")
    remove(f'{name}.pdf')
    removedirs(name)

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
        pre_name = message.text.split(' ')
        name = '_'.join(pre_name)
        await message.answer('Қай форматта ыңғайлы?', reply_markup=kb.ziporpdf)
