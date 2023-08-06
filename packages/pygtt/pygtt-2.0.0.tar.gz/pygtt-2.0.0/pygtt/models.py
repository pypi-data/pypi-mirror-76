"""Models for pygtt."""

import datetime

import attr
from typing import List


@attr.s(auto_attribs=True, frozen=True)
class BusTime:
    """BusTime object for pygtt."""

    time: datetime.datetime
    real_time: bool = False

    def __lt__(self, other):
        """Compare two BusTime objects."""
        return self.time < other.time


@attr.s(auto_attribs=True, frozen=False)
class Bus:
    """Bus object for pygtt."""

    name: str = None
    time: List[BusTime] = []

    @property
    def first_time(self) -> datetime.datetime:
        """First time of the bus."""
        if self.time and len(self.time) > 0:
            return sorted(self.time)[0]
        return None

    def __lt__(self, other: "Bus"):
        """Compare bus with another bus."""
        return self.first_time < other.first_time


@attr.s(auto_attribs=True, frozen=False)
class Stop:
    """Stop object for pygtt."""

    name: str
    bus_list: List[Bus] = []

    @property
    def next(self):
        """Next bus to stop."""
        if self.bus_list and len(self.bus_list) > 0:
            return sorted(self.bus_list, reverse=True)[0]
        return None
