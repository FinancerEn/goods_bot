from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


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

inline_confirm_payment = InlineKeyboardMarkup(
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


def get_callback_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():

        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_url_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, url in btns.items():

        keyboard.add(InlineKeyboardButton(text=text, url=url))

    return keyboard.adjust(*sizes).as_markup()


# Создать микс из CallBack и URL кнопок
def get_inlineMix_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, value in btns.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()
