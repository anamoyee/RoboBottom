from prelude import *
from tcrutils.aevents import BaseEvent


class Event(ZooBM, BaseEvent): ...


class ModsLoadedEvent(Event): ...
