import abc
import pickle
import sqlite3
from pathlib import Path

from tau.config import MessageStoreConfig, SQLite3MessageStoreConfig
from tau.types import Message, SessionID


class MessageStore(abc.ABC):
    @abc.abstractmethod
    def save(self, session_id: SessionID, messages: list[Message]):
        pass

    @abc.abstractmethod
    def load(self, session_id: SessionID) -> list[Message]:
        pass


class MemoryMessageStore(MessageStore):
    def __init__(self):
        self.messages: dict[SessionID, list[Message]] = dict()

    def save(self, session_id: SessionID, messages: list[Message]):
        if session_id not in self.messages:
            self.messages[session_id] = []
        self.messages[session_id].extend(messages)

    def load(self, session_id: SessionID) -> list[Message]:
        return self.messages.get(session_id, [])


class SQLite3MessageStore(MessageStore):
    def __init__(self, config: SQLite3MessageStoreConfig):
        self.db_path = config.db_path
        self._init_db()

    def _init_db(self):
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    message BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_session_id ON messages (session_id)
                """
            )

    def save(self, session_id: SessionID, messages: list[Message]):
        with sqlite3.connect(self.db_path) as conn:
            for message in messages:
                obj = pickle.dumps(message)

                conn.execute(
                    """
                    INSERT INTO messages (session_id, message)
                    VALUES (?, ?)
                    """,
                    (session_id, obj),
                )

    def load(self, session_id: SessionID) -> list[Message]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT message FROM messages
                WHERE session_id = ?
                ORDER BY id ASC
                """,
                (session_id,),
            )

            return [pickle.loads(r["message"]) for r in cursor]


def create_message_store(config: MessageStoreConfig) -> MessageStore:
    if config.type == "memory":
        return MemoryMessageStore()
    elif config.type == "sqlite3":
        return SQLite3MessageStore(config)
    else:
        raise ValueError(f"Unknown message store type: {config.type}")
