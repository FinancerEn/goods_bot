from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column, String, Float, DateTime, func


class Base(DeclarativeBase):
    # Время создания записи, при изменениях фиксируем дату
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class UserFSM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    user_name: Mapped[str] = mapped_column(nullable=False)
    start: Mapped[str] = mapped_column(default="")
    payment: Mapped[str] = mapped_column(nullable=False)
    feedback: Mapped[str] = mapped_column(nullable=False)


class Cart(Base):
    __tablename__ = "cart"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    user_name: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(10), nullable=False)
    price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    image = Column(String(150), nullable=True)
    quantity: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


# @dataclass
# class OrderFSM:
#     user_id: int
#     user_name: str
#     start: str = ""
#     type_property: str = ""
#     budget: int = 0
#     district: str = ""
#     specifications: str = ""
#     custom_specification: str = ""
#     contacts: str = ""
#     present: str = ""
#     name: str = ""

#     created: datetime = datetime.now()  # Время создания заявки
#     updated: datetime = datetime.now()  # Последнее обновление заявки
