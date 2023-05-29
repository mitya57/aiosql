from datetime import date

import aiosql
import pytest
import run_tests as t
import utils as u

try:
    import pymysql as db
except ModuleNotFoundError:
    pytest.skip("missing driver: pymysql", allow_module_level=True)

DRIVER = "pymysql"

pytestmark = [
    pytest.mark.mysql,
    pytest.mark.skipif(not u.has_pkg("pytest_mysql"), reason="no pytest_mysql"),
]


@pytest.fixture
def queries():
    return t.queries(DRIVER)


@pytest.fixture
def conn(my_conn):
    return my_conn


@pytest.fixture
def conn_db(my_db):
    return my_db


def test_my_dsn(my_dsn):
    assert "user" in my_dsn and "host" in my_dsn and "port" in my_dsn


def test_my_conn(conn):
    assert conn.__module__.startswith(db.__name__)
    t.run_something(conn)


def test_my_db(conn_db):
    assert conn_db.__module__.startswith(db.__name__)
    t.run_something(conn_db)


def test_cursor(conn, queries):
    t.run_cursor(conn, queries)


def test_record_query(conn_db, my_dsn, queries):
    with db.connect(**my_dsn, cursorclass=db.cursors.DictCursor) as conn:
        t.run_record_query(conn, queries)


def test_parameterized_query(conn_db, my_dsn, queries):
    t.run_parameterized_query(conn_db, queries)


@pytest.mark.skip("pymysql issue when mogrifying because of date stuff %Y")
def test_parameterized_record_query(conn_db, my_dsn, queries):  # pragma: no cover
    with db.connect(**pymysql_db_dsn, cursorclass=db.cursors.DictCursor) as conn:
        t.run_parameterized_record_query(conn, queries, DRIVER, date)


def test_record_class_query(conn_db, queries):
    t.run_record_class_query(conn_db, queries, date)


def test_select_cursor_context_manager(conn_db, queries):
    t.run_select_cursor_context_manager(conn_db, queries, date)


def test_select_one(conn_db, queries):
    t.run_select_one(conn_db, queries)


def test_select_value(conn_db, queries):
    t.run_select_value(conn_db, queries, DRIVER)


@pytest.mark.skip("MySQL does not support RETURNING")
def test_insert_returning(conn_db, queries):  # pragma: no cover
    t.run_insert_returning(conn_db, queries, DRIVER, date)


def test_delete(conn_db, queries):
    t.run_delete(conn_db, queries)


def test_insert_many(conn_db, queries):
    t.run_insert_many(conn_db, queries, date)


def test_date_time(conn_db, queries):
    t.run_date_time(conn_db, queries, DRIVER)
