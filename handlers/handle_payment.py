# import os
# from typing import Optionalimport logging
import re
from typing import Any
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from filters.config import GROUP_ID
from filters.chat_types import ChatTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import UserFSM
from dotenv import load_dotenv

from kbds import inline

load_dotenv()

# Создаем роутер
handle_payment_router = Router()
handle_payment_router.message.filter(ChatTypeFilter(["private"]))


def safe_message(text: str) -> str:
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return ''.join(
        f'\\{char}' if char in escape_chars else char
        for char in text
    )

# def escape_markdown(text: Any) -> str:
#     """
#     Экранирует спецсимволы для Telegram MarkdownV2.
#     Преобразует None в пустую строку.
#     """
#     if not isinstance(text, str):
#         text = str(text) if text is not None else ""
#     return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)


# Определяем состояния пользователя
class UserState(StatesGroup):
    clicked_buttons = State()  # Список нажатых кнопок
    feedback = State()
    name = State()
    contacts = State()


BUTTONS = {
    "main_payment": "💳 Оплата",
    # "main_feedback": "📢 Связаться с оператором",
    "main_cart": "🛒 Корзина",
    "main_products": "✅ Посмотреть товары"
}


@handle_payment_router.callback_query(lambda c: c.data == "main_feedback")
async def handle_feedback_main(callback: CallbackQuery, state: FSMContext):
    await state.update_data(feedback="📢 Связаться с оператором")
    await state.set_state(UserState.name)
    await callback.message.answer('Введите ваше имя и отчество')


@handle_payment_router.message(UserState.name, F.text)
async def handle_name_main(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserState.contacts)

    await message.answer(
        '📞 Теперь укажите ваш номер телефона и удобный способ связи (Telegram, WhatsApp):')


@handle_payment_router.message(UserState.contacts, F.text)
async def handle_contacts_main(message: Message, state: FSMContext):
    await state.update_data(contacts=message.text)
    await message.answer("✅ Нажмите 'Отправить заявку', чтобы подтвердить.",
                         reply_markup=inline.inline_confirm_payment)


@handle_payment_router.callback_query(F.data == "confirm_request", UserState.contacts)
async def confirm_request(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession  # Добавляем сессию как зависимость
):
    if isinstance(callback.message, Message):
        # 1. Получаем данные из FSM
        data = await state.get_data()

        new_order = UserFSM(
            user_id=callback.from_user.id,
            user_name=callback.from_user.full_name,
            name=data.get("name"),
            contacts=data.get("contacts"),
            feedback=data.get("feedback"),
        )

        async with session.begin():
            session.add(new_order)
        await session.commit()

        # Формируем сообщение для группы
        order_info = (
            "🛒 *Новый запрос в боте\!*\n"
            f"👤 *ID:* `{safe_message(str(callback.from_user.id))}`\n"
            f"👤 *Имя пользователя:* `{safe_message(callback.from_user.full_name)}`\n"
            f"👤 *Имя:* `{safe_message(str(data.get('name', '—')))}`\n"
            f"👤 *Контакты:* `{safe_message(str(data.get('contacts', '—')))}`"
        )

        # Отправляем в группу
        if GROUP_ID and callback.bot:
            try:
                await callback.bot.send_message(
                    chat_id=int(GROUP_ID),
                    text=order_info,
                    parse_mode="MarkdownV2"
                )
            except Exception as e:
                print(f"Ошибка отправки: {e}")
                await callback.answer("Сообщение не доставлено", show_alert=True)
                return

        # 6. Подтверждаем пользователю
        await callback.message.answer("Оператор получил ваш запрос! ✅")
        await state.clear()
        await callback.answer()


# # Обработчик нажатия на кнопки "main_..."
# @handle_payment_router.callback_query(F.data.startswith("main_"))
# async def handle_main_buttons(callback: CallbackQuery, state: FSMContext):
#     button_type = callback.data  # Получаем callback_data
#     data = await state.get_data()
#     clicked_buttons = data.get("clicked_buttons", [])

#     # Добавляем только уникальные кнопки
#     if "main_" not in clicked_buttons:
#         clicked_buttons.append(button_type)
#     # # Добавляем кнопку в список
#     # clicked_buttons.append(button_type)

#     await state.update_data(clicked_buttons=clicked_buttons)

#     # Проверяем, есть ли сообщение
#     if callback.message is None:
#         await callback.answer()  # Просто закрываем callback-запрос
#         return
#     # Если нажали "📢 Связаться с оператором", отправляем кнопку подтверждения
#     if button_type == "main_feedback":
#         await state.set_state(UserState.contac)  # Ждём подтверждения
#         await callback.message.answer("Введите ваше имя и фамилию:")
#     else:
#         await callback.answer()
# __________________________


# @handle_payment_router.callback_query(F.data == "confirm_request", UserState.feedback)
# async def confirm_request(
#     callback: CallbackQuery,
#     state: FSMContext,
#     session: AsyncSession  # Добавляем сессию как зависимость
# ):
#     # 1. Получаем данные из FSM
#     data = await state.get_data()
#     clicked_buttons = data.get("clicked_buttons", [])

#     # 2. Форматируем кнопки в читаемый вид
#     formatted_buttons = []
#     for btn in clicked_buttons:
#         # Берем читаемое название из словаря или оставляем оригинальное
#         formatted_buttons.append(BUTTONS.get(btn, btn.replace('main_', '')))

#     if not clicked_buttons:
#         await callback.answer("Нет данных для отправки", show_alert=True)
#         return

#     # 2. Формируем сообщение для группы
#     order_info = (
#         f"🛒 *Новый запрос в боте!*\n"
#         f"👤 ID: `{callback.from_user.id}`\n"
#         f"👤 Имя: `{callback.from_user.full_name}`\n"
#         f"📋 Нажатые кнопки:\n" +
#         "\n".join([f"🔹 `{btn.replace('main_', '')}`" for btn in clicked_buttons])
#     )

#     # 3. Сохраняем в PostgreSQL
#     try:
#         new_request = UserFSM(
#             user_id=callback.from_user.id,
#             user_name=callback.from_user.full_name,
#             request_data=", ".join(clicked_buttons),  # Сохраняем все нажатые кнопки
#             feedback="Подтвержденная заявка"  # Тип запроса
#         )

#         session.add(new_request)
#         await session.commit()
#     except Exception as db_error:
#         await session.rollback()
#         print(f"Ошибка БД: {db_error}")
#         await callback.answer("Ошибка обработки запроса", show_alert=True)
#         return

#     # 4. Отправляем в группу
#     if GROUP_ID_ENV and callback.bot:
#         try:
#             await callback.bot.send_message(
#                 chat_id=int(GROUP_ID_ENV),
#                 text=order_info,
#                 parse_mode="Markdown"
#             )
#         except Exception as e:
#             print(f"Ошибка отправки: {e}")
#             await callback.answer("Сообщение не доставлено", show_alert=True)
#             return
#     else:
#         print(f"GROUP_ID_ENV: {GROUP_ID_ENV}, bot: {callback.bot}")
#         await callback.answer("Ошибка конфигурации", show_alert=True)
#         return

#     # 5. Отправляем подтверждение пользователю
#     await callback.message.answer("Оператор получил ваш запрос! ✅")
#     await state.clear()
#     await callback.answer()
