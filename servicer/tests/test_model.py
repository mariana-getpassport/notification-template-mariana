"""Test the ORM model."""

import orm
import pytest
import sqlalchemy as sa
from orm.meta import Base
from orm.session import DBSession
from package_server import model
from sqlalchemy_utils import create_database, database_exists

DB_TEST_URL = "postgresql+psycopg2://postgres:postgres@localhost/testdb"


@pytest.fixture(name="empty_engine")
def fixture_empty_engine() -> sa.engine.Engine:
    """Get an empty database.

    If the database doesn't exist it creates it. It recreates the tables.
    """
    engine: sa.engine.Engine = orm.get_engine()

    # NOTE:  This is deprecated, so we probably want to have the ORM return db_url as well as engine
    if not database_exists(DB_TEST_URL):
        create_database(DB_TEST_URL)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return engine


def test_category_str() -> None:
    """Test BookCategory.__str__() method."""
    name: str = "Mystery"
    category = model.BookCategory(name=name)
    category_str: str = str(category)
    assert "BookCategory" in category_str
    assert name in category_str


def test_category_repr() -> None:
    """Test BookCategory.__repr__() method."""
    category = model.BookCategory(name="Mystery")
    category_repr: str = repr(category)
    assert category_repr.startswith("BookCategory(")
    assert "name=" in category_repr


def test_book_repr() -> None:
    """Test Book.__repr__() method."""
    category = model.BookCategory(name="Mystery")
    book = model.Book(title="The Maltese Falcon", category=category)
    book_repr: str = repr(book)
    assert book_repr.startswith("Book(")
    assert "title=" in book_repr


def test_book_invalid_category(empty_engine: sa.engine.Engine) -> None:  # pylint: disable=unused-argument
    """Test model constraints for book: invalid category."""
    with pytest.raises(sa.exc.IntegrityError):
        # Pass a category ID that's not known.
        book = model.Book(title="Dracula", category_id=15)
        with DBSession() as session, session.begin():
            session.add(book)


def test_category_query(empty_engine: sa.engine.Engine) -> None:  # pylint: disable=unused-argument
    """Test basic queries by category."""
    category1 = model.BookCategory(name="Mystery")
    category2 = model.BookCategory(name="Fantasy")
    book = model.Book(title="The Maltese Falcon", category=category1)
    with DBSession() as session, session.begin():
        session.add(category1)
        session.add(category2)
        session.add(book)
    with DBSession() as session, session.begin():
        result = session.execute(sa.select(model.Book).filter_by(category=category1))
        assert len(result.all()) == 1
        result = session.execute(sa.select(model.Book).filter_by(category=category2))
        assert len(result.all()) == 0


def test_category_null_name(empty_engine: sa.engine.Engine) -> None:  # pylint: disable=unused-argument
    """Test model constraints for book category: null name."""
    with pytest.raises(sa.exc.IntegrityError):
        # Omit non-nullable column BookCategory.name.
        category = model.BookCategory()
        with DBSession() as session, session.begin():
            session.add(category)


def test_category_long_name(empty_engine: sa.engine.Engine) -> None:  # pylint: disable=unused-argument
    """Test model constraints for book category: long name."""
    with pytest.raises(sa.exc.DataError):
        # Pass a string longer than the limit specified in model.
        category = model.BookCategory(name="S" * 33)
        with DBSession() as session, session.begin():
            session.add(category)


def test_delete_tables(empty_engine: sa.engine.Engine) -> None:  # pylint: disable=unused-argument
    """Test delete_tables()."""
    assert len(model.get_tables()) > 0
    model.delete_tables()
    assert len(model.get_tables()) == 0


def test_create_tables(empty_engine: sa.engine.Engine) -> None:
    """Test create_tables()."""
    model.delete_tables()
    assert len(model.get_tables(empty_engine)) == 0
    model.create_tables()
    assert len(model.get_tables(empty_engine)) > 0


def test_add_data(empty_engine: sa.engine.Engine) -> None:  # pylint: disable=unused-argument
    """Test add_data()."""
    model.add_data()
    with DBSession() as session, session.begin():
        result = session.execute(sa.select(model.BookCategory))
        assert len(result.all()) > 0
        result = session.execute(sa.select(model.Book))
        assert len(result.all()) > 0
