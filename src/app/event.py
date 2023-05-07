from abc import ABC, abstractmethod

import tcod


class AbstractEventHandler(ABC):

    @abstractmethod
    def handle_event(self, event: tcod.event.Event):
        ...


class ExitEventHandler(AbstractEventHandler):

    def handle_event(self, event: tcod.event.Event):
        if isinstance(event, tcod.event.Quit):
            raise SystemExit()


