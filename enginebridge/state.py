"""Shared per-host admission. Never stores prompts or credentials."""
import sqlite3
import time
import uuid
from pathlib import Path


class State:
    def __init__(self, path):
        path = Path(path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.path = path
        with self.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS pools (pool TEXT PRIMARY KEY, blocked INTEGER DEFAULT 0, until REAL DEFAULT 0, owner TEXT, lease REAL DEFAULT 0)")
        path.chmod(0o600)

    def connect(self):
        return sqlite3.connect(self.path, timeout=10)

    def status(self):
        with self.connect() as db:
            db.row_factory = sqlite3.Row
            return [dict(r) for r in db.execute("SELECT * FROM pools ORDER BY pool")]

    def block(self, pool, blocked=True):
        with self.connect() as db:
            db.execute("INSERT INTO pools(pool,blocked) VALUES (?,?) ON CONFLICT(pool) DO UPDATE SET blocked=excluded.blocked", (pool, int(blocked)))

    def cooldown(self, pool, seconds):
        with self.connect() as db:
            db.execute("INSERT INTO pools(pool,until) VALUES (?,?) ON CONFLICT(pool) DO UPDATE SET until=MAX(pools.until, excluded.until)", (pool, time.time() + seconds))

    def acquire(self, pool, seconds):
        owner = uuid.uuid4().hex
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("INSERT OR IGNORE INTO pools(pool) VALUES (?)", (pool,))
            blocked, until, lease = db.execute("SELECT blocked,until,lease FROM pools WHERE pool=?", (pool,)).fetchone()
            if blocked or until > time.time() or lease > time.time():
                return None
            db.execute("UPDATE pools SET owner=?,lease=? WHERE pool=?", (owner, time.time() + seconds, pool))
        return owner

    def release(self, pool, owner):
        with self.connect() as db:
            db.execute("UPDATE pools SET owner=NULL,lease=0 WHERE pool=? AND owner=?", (pool, owner))
