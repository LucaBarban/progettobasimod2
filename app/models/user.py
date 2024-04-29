from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from typing import Optional
import datetime

# TODO: aggiungere colonna token (nullable + indice) e logingdate (not null) al db

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[date]
    last_logged_in_at: Mapped[datetime.datetime]
    balance: Mapped[int]
    seller: Mapped[bool]
    token: Mapped[Optional[str]]

    def __init__(self, username: str, first_name: str, last_name: str, password: str, created_at: datetime.datetime, last_logged_in_at:datetime.datetime, balance:int, seller:bool, token:str):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.created_at = created_at
        self.last_logged_in_at = last_logged_in_at
        self.balance = balance
        self.seller = seller
        self.token = token

    def __repr__(self) -> str:
        return "User: '%s' ('%s', '%s' at '%s' s:'%s') -> bal='%s'<br>pwd: '%s'<br>token: '%s'" % (self.username, self.first_name, self.last_name, str(self.last_logged_in_at), self.seller, self.balance, self.password, self.token)
