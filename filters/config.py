import os
from typing import Optional

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения 'TOKEN' не задана.")


def parse_group_id(env_value: Optional[str]) -> Optional[int]:
    """Безопасное преобразование GROUP_ID из env."""
    if env_value is None:
        return None
    try:
        return int(env_value)
    except ValueError:
        return None


GROUP_ID: Optional[int] = parse_group_id(os.getenv("GROUP_ID"))


# import os
# from typing import Optional

# TOKEN = os.getenv("TOKEN")
# if not TOKEN:
#     raise ValueError("Переменная окружения 'TOKEN' не задана.")

# GROUP_ID_ENV = os.getenv("GROUP_ID")
# GROUP_ID: Optional[int] = int(GROUP_ID_ENV) if GROUP_ID_ENV and GROUP_ID_ENV.isdigit() else None
