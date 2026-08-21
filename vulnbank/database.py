from __future__ import annotations

import sqlite3

_conn: sqlite3.Connection | None = None


def get_db() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = _build()
    return _conn


def _build() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE users (
            id       INTEGER PRIMARY KEY,
            username TEXT    NOT NULL,
            email    TEXT    NOT NULL,
            role     TEXT    NOT NULL DEFAULT 'user',
            ssn      TEXT,
            balance  REAL    DEFAULT 0,
            password TEXT    NOT NULL
        );

        CREATE TABLE accounts (
            id             INTEGER PRIMARY KEY,
            owner_id       INTEGER NOT NULL,
            type           TEXT    NOT NULL,
            balance        REAL    DEFAULT 0,
            routing        TEXT,
            account_number TEXT
        );

        INSERT INTO users VALUES (1,'alice',  'alice@vulnbank.com',  'user', '123-45-6789', 5000.00, 'password123');
        INSERT INTO users VALUES (2,'bob',    'bob@vulnbank.com',    'user', '987-65-4321',12500.00, 'hunter2');
        INSERT INTO users VALUES (3,'charlie','charlie@vulnbank.com','user', '555-44-3333',  750.00, 'ilovecats');
        INSERT INTO users VALUES (4,'admin',  'admin@vulnbank.com',  'admin','000-00-0001',    0.00, 'Adm1n$ecure!');

        INSERT INTO accounts VALUES (101,1,'checking', 5000.00,'021000021','4111111111110001');
        INSERT INTO accounts VALUES (102,1,'savings', 22000.00,'021000021','4111111111110002');
        INSERT INTO accounts VALUES (103,2,'checking',12500.00,'021000021','4111111111110003');
        INSERT INTO accounts VALUES (104,3,'checking',  750.00,'021000021','4111111111110004');
    """)
    conn.commit()
    return conn
