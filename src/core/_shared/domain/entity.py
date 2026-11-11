import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID
from src.core._shared.events.message_bus import MessageBus
from src.core._shared.events.event import Event
from src.core._shared.events.abstract_message_bus import AbstractMessageBus

from src.core._shared.domain.notification import Notification


@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID = field(default_factory=uuid.uuid4)
    notification: Notification = field(default_factory=Notification)
    events: list[Event] = field(default_factory=list, init=False)
    message_bus: AbstractMessageBus = field(default_factory=MessageBus, init=True, compare=False)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def dispatch(self, event: Event) -> None:
        self.events.append(event)
        self.message_bus.handle(self.events)

    @abstractmethod
    def validate(self):
        raise NotImplementedError
