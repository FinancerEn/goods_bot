from aiogram import Router, F
from aiogram.types import FSInputFile, CallbackQuery, Message
from filters.chat_types import ChatTypeFilter

from dotenv import load_dotenv

from text_message import text
from kbds import inline

load_dotenv()


handle_products_router = Router()
handle_products_router.message.filter(ChatTypeFilter(['private']))


@handle_products_router.callback_query(F.data.startswith('main_view_products'))
async def handle_view_products(callback: CallbackQuery):
    '''Обработчик выбора типа товара'''
    if not isinstance(callback.message, Message):
        return await callback.answer("Ошибка: невозможно отправить сообщение")

    await callback.message.answer(
        text.start_products_text, reply_markup=inline.inline_products
    )
    await callback.answer()


@handle_products_router.callback_query(F.data.startswith('products_loft'))
async def handle_loft(callback: CallbackQuery):
    '''Обработчик выбора типа товара'''
    photo = FSInputFile('images/commode_loft.webp')
    if not isinstance(callback.message, Message):
        return await callback.answer("Ошибка: невозможно отправить сообщение")

    await callback.message.answer_photo(photo)
    await callback.message.answer(
        text.start_products_text, reply_markup=inline.inline_back_commod
    )
    await callback.answer()


@handle_products_router.callback_query(F.data.startswith('products_scandi'))
async def handle_scandi(callback: CallbackQuery):
    '''Обработчик выбора типа товара'''
    photo = FSInputFile('images/commode_scandi.webp')
    if not isinstance(callback.message, Message):
        return await callback.answer("Ошибка: невозможно отправить сообщение")

    await callback.message.answer_photo(photo)
    await callback.message.answer(
        text.commode_scandi_text, reply_markup=inline.inline_back_commod
    )
    await callback.answer()


@handle_products_router.callback_query(F.data.startswith('products_retro'))
async def handle_retro(callback: CallbackQuery):
    '''Обработчик выбора типа товара'''
    photo = FSInputFile('images/commode_retro.webp')
    if not isinstance(callback.message, Message):
        return await callback.answer("Ошибка: невозможно отправить сообщение")

    await callback.message.answer_photo(photo)
    await callback.message.answer(
        text.commode_retro_text, reply_markup=inline.inline_back_commod
    )
    await callback.answer()


@handle_products_router.callback_query(F.data.startswith('products_modern'))
async def handle_modern(callback: CallbackQuery):
    '''Обработчик выбора типа товара'''
    photo = FSInputFile('images/commod_modern.webp')
    if not isinstance(callback.message, Message):
        return await callback.answer("Ошибка: невозможно отправить сообщение")

    await callback.message.answer_photo(photo)
    await callback.message.answer(
        text.commod_modern_text, reply_markup=inline.inline_back_commod
    )
    await callback.answer()


@handle_products_router.callback_query(F.data.startswith('products_provence'))
async def handle_provence(callback: CallbackQuery):
    '''Обработчик выбора типа товара'''
    photo = FSInputFile('images/commod_provence.webp')
    if not isinstance(callback.message, Message):
        return await callback.answer("Ошибка: невозможно отправить сообщение")

    await callback.message.answer_photo(photo)
    await callback.message.answer(
        text.commod_provence_text, reply_markup=inline.inline_back_commod
    )
    await callback.answer()


@handle_products_router.callback_query(F.data.startswith('products_Industrial'))
async def handle_Industrial(callback: CallbackQuery):
    '''Обработчик выбора типа товара'''
    photo = FSInputFile('images/commod_Industrial.webp')
    if not isinstance(callback.message, Message):
        return await callback.answer("Ошибка: невозможно отправить сообщение")

    await callback.message.answer_photo(photo)
    await callback.message.answer(
        text.commod_Industrial_text, reply_markup=inline.inline_back_commod
    )
    await callback.answer()


@handle_products_router.callback_query(F.data.startswith('back_main'))
async def handler_back_main(callback: CallbackQuery):
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            text.main_text, reply_markup=inline.inline_main
        )
        await callback.answer()


@handle_products_router.callback_query(F.data.startswith('back_commod'))
async def handler_back_commod(callback: CallbackQuery):
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            text.start_products_text, reply_markup=inline.inline_products
        )
        await callback.answer()
