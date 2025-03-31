import os
from typing import Optional
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from filters.chat_types import ChatTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

from text_message import text
from kbds import inline

load_dotenv()

# Загружаем GROUP_ID
GROUP_ID_ENV = os.getenv('GROUP_ID')
GROUP_ID: Optional[int] = int(GROUP_ID_ENV) if GROUP_ID_ENV and GROUP_ID_ENV.isdigit() else None

# Создаем роутер
handle_payment_router = Router()
handle_payment_router.message.filter(ChatTypeFilter(['private']))


# Определяем состояния пользователя
class UserState(StatesGroup):
    clicked_buttons = State()  # Список нажатых кнопок
    feedback = State()  # Ожидание подтверждения заявки


# Обработчик кнопки оплаты
@handle_payment_router.callback_query(F.data.startswith('main_payment'))
async def handle_payment(callback: CallbackQuery):
    if not callback.data:
        return
    if not isinstance(callback.message, Message):
        return await callback.answer("Ошибка: невозможно отправить сообщение")
    await callback.message.answer(
        text.payment_text, reply_markup=inline.inline_back_main
    )
    await callback.answer()


# Обработчик нажатия на кнопки "main_..."
@handle_payment_router.callback_query(F.data.startswith("main_"))
async def handle_main_buttons(callback: CallbackQuery, state: FSMContext):
    button_type = callback.data  # Получаем callback_data
    data = await state.get_data()
    clicked_buttons = data.get("clicked_buttons", [])

    # Добавляем кнопку в список
    clicked_buttons.append(button_type)
    await state.update_data(clicked_buttons=clicked_buttons)

    # Если нажали "📢 Связаться с оператором", отправляем кнопку подтверждения
    if button_type == "main_feedback":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✅ Подтвердить заявку", callback_data="confirm_request")]
            ]
        )
        await state.set_state(UserState.feedback)  # Ждём подтверждения
        await callback.message.answer("Нажмите кнопку ниже, чтобы отправить заявку оператору:", reply_markup=keyboard)
    else:
        await callback.answer()


@handle_payment_router.callback_query(F.data == "confirm_request", UserState.feedback)
async def confirm_request(callback: CallbackQuery, state: FSMContext):
    # 1. Получаем данные
    data = await state.get_data()
    clicked_buttons = data.get("clicked_buttons", [])

    if not clicked_buttons:
        await callback.answer("Нет данных для отправки", show_alert=True)
        return

    # 2. Формируем сообщение (как в рабочем коде)
    order_info = (
        f"🛒 *Новый запрос в боте!*\n"
        f"👤 ID: `{callback.from_user.id}`\n"
        f"👤 Имя: `{callback.from_user.full_name}`\n"
        f"📋 Нажатые кнопки:\n" +
        "\n".join([f"🔹 `{btn.replace('main_', '')}`" for btn in clicked_buttons])
    )

    # 3. Отправляем в группу (как в РАБОЧЕМ коде)
    if GROUP_ID_ENV and callback.bot:  # Используем callback.bot
        try:
            await callback.bot.send_message(
                chat_id=int(GROUP_ID_ENV),  # Явное преобразование
                text=order_info,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Ошибка: {e}")
            await callback.answer("Ошибка отправки", show_alert=True)
            return
    else:
        print(f"GROUP_ID_ENV: {GROUP_ID_ENV}, bot: {callback.bot}")
        await callback.answer("Ошибка конфигурации", show_alert=True)
        return

    # 4. Завершение (как в рабочем коде)
    await callback.message.answer("Оператор получил ваш запрос! ✅")
    await state.clear()
    await callback.answer()
