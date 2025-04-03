from aiogram import Bot
from aiogram import Bot
from typing import List


class CustomBot(Bot):
    def __init__(self, token: str):
        super().__init__(token)
        self.my_admins_list: List[int] = []
