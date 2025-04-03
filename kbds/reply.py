from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# # Клавиатура для администратора
# ADMIN_KB = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="Создать заказ"), KeyboardButton(text="Удалить заказ")],
#         [KeyboardButton(text="Просмотр заказов"), KeyboardButton(text="Назад")],
#     ],
#     resize_keyboard=True,
# )


def get_keyboard(
    *btns: str,  # принимает любое количество текстов для кнопок.
    placeholder: str = None,  # текст-подсказка в поле ввода.
    request_contact: int = None,  # индексы кнопок, которые должны запрашивать контакт или геолокацию.
    request_location: int = None,
    # кортеж, определяющий количество кнопок в каждой строке (например, (2, 1) — две кнопки в первой строке, одна во второй).
    sizes: tuple[int] = (2,),
):
    '''
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            "Отправить номер телефона",
            placeholder="Что вас интересует?",
            request_contact=4,
            sizes=(2, 2, 1)
        )
    '''
    keyboard = ReplyKeyboardBuilder()

    # Добавление кнопок:
    for index, text in enumerate(btns, start=0):

        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    # Настройка расположения и возврат клавиатуры:
    return keyboard.adjust(*sizes).as_markup(
            resize_keyboard=True, input_field_placeholder=placeholder)

    ''' adjust(*sizes) — распределяет кнопки по строкам согласно sizes.

        as_markup() — преобразует ReplyKeyboardBuilder в готовую клавиатуру.

        resize_keyboard=True — автоматически подгоняет размер кнопок.

        input_field_placeholder — устанавливает подсказку.
    '''
