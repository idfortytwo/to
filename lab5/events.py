from enum import Enum, auto
from typing import Tuple


class EventType(Enum):
    FIRE = auto()
    FALSE_ALARM = auto()
    LOCAL_THREAT = auto()


class Event:
    def __init__(self, event_type: EventType, coords: Tuple[float, float]):
        self.event_type = event_type
        self.coords = coords

    @property
    def coords(self) -> Tuple[float, float]:
        return self._coords

    @coords.setter
    def coords(self, coords):
        x, y = coords
        if (49.95855025648944 < x < 50.154564013341734) and (19.688292482742394 < y < 20.02470275868903):
            self._coords = coords
        else:
            raise ValueError('Coordinates should be between (50.154564013341734, 19.688292482742394)'
                             ' and (49.95855025648944, 20.02470275868903)')