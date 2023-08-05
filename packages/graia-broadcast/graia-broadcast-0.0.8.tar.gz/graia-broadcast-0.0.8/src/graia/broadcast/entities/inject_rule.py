from typing import Type
from pydantic import BaseModel
import abc
from .event import BaseEvent
from ..interfaces.dispatcher import DispatcherInterface
from .dispatcher import BaseDispatcher

class BaseRule(abc.ABC, BaseModel):
    target_dispatcher: BaseDispatcher

    def __init__(self, target_dispatcher: BaseDispatcher) -> None:
        self.target_dispatcher = target_dispatcher

    @abc.abstractmethod
    def check(self, event: BaseEvent, dii: DispatcherInterface) -> bool:
        pass

class SpecialEventType(BaseRule):
    target_dispatcher: BaseDispatcher

    def __init__(self, event_type: Type[BaseEvent], target_dispatcher: BaseDispatcher, specially: bool = False) -> None:
        self.target_dispatcher = target_dispatcher
        self.event_type = event_type
        self.specially = specially

    def check(self, event: BaseEvent, dii: DispatcherInterface) -> bool:
        if self.specially:
            if type(event) is self.event_type:
                return True
        else:
            if isinstance(event, self.event_type):
                return True