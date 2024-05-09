import datetime
from database_folder.core import Base
from sqlalchemy.orm import Mapped, mapped_column


class Data(Base):
    __tablename__ = 'data'
    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[str] = mapped_column()
    date: Mapped[datetime.datetime] = mapped_column()
