"""High-level Event base class implementation."""
from .utils import timestamp


class Event:
    """An Event represents an individual event from a thing."""

    name = None

    def __init__(self, data=None):
        """
        Initialize the object.
        thing -- Thing this event belongs to
        name -- name of the event
        data -- data associated with the event
        """
        self.thing = None
        self.data = data
        self.time = timestamp()

    async def as_event_description(self):
        """
        Get the event description.
        Returns a dictionary describing the event.
        """
        description = {
            self.name: {"timestamp": self.time,},
        }

        if self.data is not None:
            description[self.name]["data"] = self.data

        return description

    async def get_thing(self):
        """Get the thing associated with this event."""
        return self.thing

    async def set_thing(self, thing):
        """Set the thing associated with this event."""
        self.thing = thing

    async def get_name(self):
        """Get the event's name."""
        return self.name

    async def get_data(self):
        """Get the event's data."""
        return self.data

    async def get_time(self):
        """Get the event's timestamp."""
        return self.time


class ThingPairingEvent(Event):
    name = "thing_pairing"


class ThingPairedEvent(Event):
    name = "thing_paired"


class ThingRemovedEvent(Event):
    name = "thing_removed"
