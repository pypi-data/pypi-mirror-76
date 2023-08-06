from pygtt import BusTime
from datetime import datetime


def test_bus_time():
    bt = BusTime(datetime.strptime("12:22", "%H:%M"), True)
    assert bt.time == datetime.strptime("12:22", "%H:%M")
    assert bt.real_time


def test_bus_time_default():
    bt = BusTime(datetime.strptime("12:22", "%H:%M"))
    assert not bt.real_time


def test_bus_time_lt():
    bt1 = BusTime(datetime.strptime("12:22", "%H:%M"))
    bt2 = BusTime(datetime.strptime("12:23", "%H:%M"))
    assert bt1 <= bt2
