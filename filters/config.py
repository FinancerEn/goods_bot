import os
from typing import Optional

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения 'TOKEN' не задана.")


def parse_group_id(env_value: Optional[str]) -> int:
    """Безопасное преобразование GROUP_ID из env."""
    if env_value is None:
        raise ValueError("GROUP_ID не найден в переменных окружения!")
    try:
        return int(env_value)
    except ValueError:
        raise ValueError(f"GROUP_ID должен быть числом, а не '{env_value}'")


GROUP_ID: int = parse_group_id(os.getenv("GROUP_ID"))


# import os
# from typing import Optional

# TOKEN = os.getenv("TOKEN")
# if not TOKEN:
#     raise ValueError("Переменная окружения 'TOKEN' не задана.")

# GROUP_ID_ENV = os.getenv("GROUP_ID")
# GROUP_ID: Optional[int] = int(GROUP_ID_ENV) if GROUP_ID_ENV and GROUP_ID_ENV.isdigit() else None
