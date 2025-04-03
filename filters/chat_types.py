# Фильтруем события по группам, чатам отдельно.
# Импортируем Filter базовый класс.
from aiogram.filters import Filter
from aiogram.types import Message
from filters.bot import CustomBot
# from aiogram.exceptions import TelegramBadRequest
# from aiogram.types import ChatMemberAdministrator, ChatMemberOwner


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    async def __call__(self, message: Message, bot: CustomBot) -> bool:
        if not message.from_user:  # Проверяем, есть ли отправитель сообщения
            return False
        return message.from_user.id in bot.my_admins_list


# class IsAdmin(Filter):
#     async def __call__(self, message: Message, bot: Bot) -> bool:
#         if not message.from_user:  # Проверяем, есть ли вообще пользователь
#             return False

#         chat_id = message.chat.id  # ID чата (группы)
#         try:
#             admins = await bot.get_chat_administrators(chat_id)
#         except TelegramBadRequest:
#             return False  # Если ошибка, значит, бот не админ

#         # Проверяем, есть ли у пользователя права администратора
#         return any(
#             isinstance(admin, (ChatMemberOwner, ChatMemberAdministrator)) and admin.user.id == message.from_user.id
#             for admin in admins
#         )
