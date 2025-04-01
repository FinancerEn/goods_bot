import os
from typing import Optional
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from filters.chat_types import ChatTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import UserFSM
from dotenv import load_dotenv

from text_message import text
from kbds import inline

load_dotenv()

# Загружаем GROUP_ID
GROUP_ID_ENV = os.getenv("GROUP_ID")
GROUP_ID: Optional[int] = (
    int(GROUP_ID_ENV) if GROUP_ID_ENV and GROUP_ID_ENV.isdigit() else None
)

# Создаем роутер
handle_payment_router = Router()
handle_payment_router.message.filter(ChatTypeFilter(["private"]))


# Определяем состояния пользователя
class UserState(StatesGroup):
    clicked_buttons = State()  # Список нажатых кнопок
    feedback = State()
    created_at = State()
    updated_at = State()


BUTTONS = {
    "main_payment": "💳 Оплата",
    "main_feedback": "📢 Связаться с оператором",
    "main_cart": "🛒 Корзина",
    "main_products": "✅ Посмотреть товары"
}


# Обработчик нажатия на кнопки "main_..."
@handle_payment_router.callback_query(F.data.startswith("main_"))
async def handle_main_buttons(callback: CallbackQuery, state: FSMContext):
    button_type = callback.data  # Получаем callback_data
    data = await state.get_data()
    clicked_buttons = data.get("clicked_buttons", [])

    # Добавляем только уникальные кнопки
    if "main_" not in clicked_buttons:
        clicked_buttons.append(button_type)
    # # Добавляем кнопку в список
    # clicked_buttons.append(button_type)

    await state.update_data(clicked_buttons=clicked_buttons)

    # Если нажали "📢 Связаться с оператором", отправляем кнопку подтверждения
    if button_type == "main_feedback":
        await state.set_state(UserState.feedback)  # Ждём подтверждения
        await callback.message.answer("Нажмите кнопку ниже, чтобы отправить заявку оператору:",
                                      reply_markup=inline.inline_confirm_payment)
    else:
        await callback.answer()


@handle_payment_router.callback_query(F.data == "confirm_request", UserState.feedback)
async def confirm_request(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession  # Добавляем сессию как зависимость
):
    # 1. Получаем данные из FSM
    data = await state.get_data()
    clicked_buttons = data.get("clicked_buttons", [])

    if not clicked_buttons:
        await callback.answer("Нет данных для отправки", show_alert=True)
        return

    # 2. Формируем список с читаемыми названиями кнопок
    formatted_buttons = [BUTTONS.get(btn, "Неизвестная кнопка") for btn in clicked_buttons]

    # 3. Формируем сообщение для группы
    order_info = (
        f"🛒 *Новый запрос в боте!*\n"
        f"👤 ID: `{callback.from_user.id}`\n"
        f"👤 Имя: `{callback.from_user.full_name}`\n"
        f"📋 Нажатые кнопки:\n" +
        "\n".join([f"🔹 {btn}" for btn in formatted_buttons])
    )

    # 4. Сохраняем в PostgreSQL
    try:
        new_request = UserFSM(
            user_id=callback.from_user.id,
            user_name=callback.from_user.full_name,
            request_data=", ".join(formatted_buttons),  # Сохраняем реальные названия кнопок
            feedback="Подтвержденная заявка"
        )

        session.add(new_request)
        await session.commit()
    except Exception as db_error:
        await session.rollback()
        print(f"Ошибка БД: {db_error}")
        await callback.answer("Ошибка обработки запроса", show_alert=True)
        return

    # 5. Отправляем в группу
    try:
        await callback.bot.send_message(
            chat_id=int(GROUP_ID_ENV),
            text=order_info,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        await callback.answer("Сообщение не доставлено", show_alert=True)
        return

    # 6. Подтверждаем пользователю
    await callback.message.answer("Оператор получил ваш запрос! ✅")
    await state.clear()
    await callback.answer()


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
