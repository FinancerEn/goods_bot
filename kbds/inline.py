from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class MainCallback(CallbackData, prefix="main_"):
    name: str


inline_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Посмотреть товары", callback_data="main_view_products")],
        [InlineKeyboardButton(text="💳 Оплата", callback_data="main_payment")],
        [InlineKeyboardButton(text="🛒 Корзина", callback_data="_main_cart")],
        [InlineKeyboardButton(text="📢 Связаться с оператором", callback_data="main_feedback")],
    ],
)


inline_products = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Комод Лофт Элеганс", callback_data="products_loft")],
        [InlineKeyboardButton(text="Комод Сканди Классик", callback_data="products_scandi")],
        [InlineKeyboardButton(text="Комод Ретро Винтаж", callback_data="products_retro")],
        [InlineKeyboardButton(text="Комод Модерн Лайн", callback_data="products_modern")],
        [InlineKeyboardButton(text="Комод Прованс Шарм", callback_data="products_provence")],
        [InlineKeyboardButton(text="Комод Индастриал Стайл", callback_data="products_Industrial")],
        [InlineKeyboardButton(text="Назад в главное меню", callback_data="back_main")],
    ],
)

inline_back_commod = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить заявку", callback_data="confirm_request")],
    ],
)

inline_back_commod = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад к комодам", callback_data="back_commod")],
    ],
)

inline_back_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад в главное меню", callback_data="back_main")],
    ],
)
