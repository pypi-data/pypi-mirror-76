from pygtt import Bus
import datetime


def test_bus():
    bus = Bus(
        "58b",
        [
            datetime.datetime(2020, 12, 1),
            datetime.datetime(2019, 2, 16),
            datetime.datetime(2019, 5, 12),
        ],
    )
    assert bus.name == "58b"
    assert bus.time == [
        datetime.datetime(2020, 12, 1),
        datetime.datetime(2019, 2, 16),
        datetime.datetime(2019, 5, 12),
    ]
    assert bus.first_time == datetime.datetime(2019, 2, 16)


def test_bus_lt():
    bus1 = Bus(
        "58b",
        [
            datetime.datetime(2020, 12, 1),
            datetime.datetime(2019, 2, 16),
            datetime.datetime(2019, 5, 12),
        ],
    )
    bus2 = Bus("12", [datetime.datetime(2019, 12, 1), datetime.datetime(2018, 2, 16)])
    bus3 = Bus("M1", None)
    bus4 = Bus("M2", [])
    assert bus2 < bus1
    assert bus1 < bus3
    assert bus4 >= bus3


def test_bus_lt_none():
    bus1 = Bus("1", [])
    bus2 = Bus("2", None)
    assert bus1.first_time is None
    assert bus2.first_time is None
