from random import shuffle
from typing import Callable, List, Self

from app.database import db
from app.models.book import Book
from app.models.genre import Genre

AllowedExtensions = {'png', 'jpeg', 'jpg'}

class BookListByGenre:
    def __init__(self) -> None:
        self.genres = db.session.query(Genre).all()
        for x in self.genres:
            shuffle(x.books)

    def prune(self, predicate: Callable[[List[Book]], bool]) -> Self:
        self.genres = [v for v in self.genres if not predicate(v.books)]
        return self

    def normalize(self, apply: Callable[[List[Book]], List[Book]]) -> Self:
        for v in self.genres:
            v.books = apply(v.books)
        return self

    def dump(self) -> List[Genre]:
        return self.genres
