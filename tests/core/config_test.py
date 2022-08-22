from __future__ import annotations

from pydantic import PostgresDsn

from app.core.config import Settings


def test_uri_validator():
    db_uri = 'postgresql://user:pw@host/db'  # pragma: allowlist secret
    settings = Settings(DATABASE_URI=db_uri)
    assert settings.DATABASE_URI == db_uri


def test_pg_dsn():
    db_uri = 'postgresql://user:pw@host:5432/db'  # pragma: allowlist secret
    settings = Settings(
        POSTGRES_SERVER='host',
        POSTGRES_USER='user',
        POSTGRES_PASSWORD='pw',  # pragma: allowlist secret
        POSTGRES_DB='db',
        POSTGRES_PORT='5432',
    )
    assert isinstance(settings.DATABASE_URI, PostgresDsn)
    assert settings.DATABASE_URI == db_uri
