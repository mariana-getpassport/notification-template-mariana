"""ORM model."""

import orm
import sqlalchemy
from orm.meta import Base
from orm.mixins import PKMixin, SoftDeleteMixin, TimestampsMixin
from orm.session import DBSession
from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship


class BookCategory(TimestampsMixin, SoftDeleteMixin, Base):
    """Book Category."""

    __tablename__ = "book_category"

    id: int = Column(Integer, primary_key=True)  # noqa: A003
    name: str = Column(Unicode(32), nullable=False)
    books: list["Book"] = relationship("Book", back_populates="category")

    def __str__(self):
        """Return readable representation of instance."""
        return f"BookCategory ({self.name})"

    def __repr__(self):
        """Return printable representation of instance."""
        return f"BookCategory(id={self.id!r}, name={self.name!r})"


class Book(PKMixin, TimestampsMixin, SoftDeleteMixin, Base):
    """Book."""

    __tablename__ = "book"

    title: str = Column(Unicode(128), nullable=False)
    category_id: int = Column(Integer, ForeignKey("book_category.id"))
    category: BookCategory = relationship("BookCategory", back_populates="books")

    def __repr__(self):
        """Return printable representation of instance."""
        return f"Book(id={self.id!r}, title={self.title!r}, category={self.category.name!r})"


def delete_tables():
    """Delete all tables from database."""
    engine = orm.get_engine()
    Base.metadata.drop_all(engine)


def create_tables():
    """Create database tables."""
    engine = orm.get_engine()
    Base.metadata.create_all(engine)


def get_tables(engine: sqlalchemy.engine.Engine = None) -> list[str]:
    """Get name of created tables."""
    if engine is None:
        engine = orm.get_engine()
    inspected_engine = sqlalchemy.inspect(engine)
    tables = Base.metadata.tables  # All tables defined in model.
    return [table for table in tables if inspected_engine.has_table(table)]


def add_data():
    """Populate database with some data."""
    mystery = BookCategory(name="Mystery")
    science_fiction = BookCategory(name="Science Fiction")
    self_help = BookCategory(name="Self Help")
    books = [
        Book(title="The Maltese Falcon", category=mystery),
        Book(title="Murder on the Orient Express", category=mystery),
        Book(title="The Hound of the Baskervilles", category=mystery),
        Book(title="The Hitchhiker's Guide to the Galaxy", category=science_fiction),
        Book(title="Ender's Game", category=science_fiction),
        Book(title="The Dune Chronicles", category=science_fiction),
        Book(title="The 7 Habits of Highly Effective People", category=self_help),
        Book(title="How to Win Friends and Influence People", category=self_help),
        Book(title="Man's Search for Meaning", category=self_help),
    ]
    with DBSession() as session, session.begin():
        session.add_all([mystery, science_fiction, self_help])
        session.add_all(books)
