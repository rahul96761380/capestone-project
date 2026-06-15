"""
db.py — PostgreSQL connection pool for Day 04 eComBot
-----------------------------------------------------
Shared thread-safe PostgreSQL connection pool.

Public API:
    query_one(sql, params)  -> dict | None
    query_all(sql, params)  -> list[dict]
    execute(sql, params)    -> int
    check_connection()      -> bool
"""

from contextlib import contextmanager
from typing import Any, Generator
import logging

from psycopg2 import pool as pg_pool
from psycopg2.extras import RealDictCursor

from ecombot.src.config.settings import settings

log = logging.getLogger(__name__)

_pool: pg_pool.ThreadedConnectionPool | None = None


def _get_pool() -> pg_pool.ThreadedConnectionPool:
    """
    Lazily create a shared connection pool.
    """
    global _pool

    if _pool is None:
        _pool = pg_pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=settings.pg_dsn,
        )

        log.info(
            "PostgreSQL pool created (%s:%s/%s)",
            settings.pg_host,
            settings.pg_port,
            settings.pg_db,
        )

    return _pool


@contextmanager
def _get_conn() -> Generator:
    """
    Lease a connection from the pool.
    Commits on success and rolls back on failure.
    """
    conn_pool = _get_pool()
    conn = conn_pool.getconn()

    try:
        yield conn
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn_pool.putconn(conn)


def query_one(
    sql: str,
    params: tuple[Any, ...] | None = None,
) -> dict[str, Any] | None:
    """
    Execute SELECT and return one row.
    """
    with _get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            row = cur.fetchone()

            if row is None:
                return None

            return dict(row)


def query_all(
    sql: str,
    params: tuple[Any, ...] | None = None,
) -> list[dict[str, Any]]:
    """
    Execute SELECT and return all rows.
    """
    with _get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)

            return [dict(row) for row in cur.fetchall()]


def execute(
    sql: str,
    params: tuple[Any, ...] | None = None,
) -> int:
    """
    Execute INSERT/UPDATE/DELETE.
    Returns affected row count.
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.rowcount


def check_connection() -> bool:
    """
    PostgreSQL health check.
    """
    try:
        with _get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")

        return True

    except Exception as exc:
        log.warning(
            "PostgreSQL health check failed: %s",
            exc,
        )
        return False


def close_pool() -> None:
    """
    Gracefully close all pooled connections.
    """
    global _pool

    if _pool is not None:
        _pool.closeall()
        _pool = None

        log.info("PostgreSQL connection pool closed")