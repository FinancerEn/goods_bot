from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, Column, String, Text, Float, DateTime, func, Integer


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class UserFSM(Base):
    __tablename__ = "user_fsm"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    user_name: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    payment: Mapped[str] = mapped_column(String, nullable=True)
    feedback: Mapped[str] = mapped_column(String, nullable=True)
    contacts: Mapped[str] = mapped_column(String(255), nullable=False)
    request_data: Mapped[str] = mapped_column(String, nullable=True)


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    image: Mapped[str] = mapped_column(String(150))


# class Cart(Base):
#     __tablename__ = "cart"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(Integer, nullable=True)
#     user_name: Mapped[str] = mapped_column(String, nullable=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=True)
#     description: Mapped[str] = mapped_column(String(10), nullable=True)
#     price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=True)
#     image = Column(String(150), nullable=True)
#     quantity: Mapped[int] = mapped_column(Integer, nullable=True)

#     # Поля времени
#     created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
#     updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


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
