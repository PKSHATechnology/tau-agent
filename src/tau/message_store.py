import abc

from tau.config import MessageStoreConfig
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


def create_message_store(config: MessageStoreConfig) -> MessageStore:
    if config.type == "memory":
        return MemoryMessageStore()
    else:
        raise ValueError(f"Unknown message store type: {config.type}")
