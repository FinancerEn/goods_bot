# Этот файл расширяет стандартный Bot из aiogram, добавляя список админов.
from aiogram import Bot
from aiogram import Bot
from typing import List


# Создаём свой класс CustomBot, который наследуется от Bot.
# Добавляем атрибут my_admins_list, где будут храниться ID админов.
class CustomBot(Bot):
    def __init__(self, token: str):
        super().__init__(token)
        self.my_admins_list: List[int] = []
