from pygtt import Stop, Bus
from datetime import datetime
import copy


def test_stop():
    stop = Stop("1234", [])
    assert stop.name == "1234"
    assert stop.bus_list == []
    assert stop.next is None


def test_stop_next():
    stop = Stop(
        "1234",
        [
            Bus("1", [datetime.fromtimestamp(1237), datetime.fromtimestamp(1236)]),
            Bus("2", [datetime.fromtimestamp(1235), datetime.fromtimestamp(1234)]),
        ],
    )
    assert stop.next.name == "2"
    assert stop.next.first_time == datetime.fromtimestamp(1234)


def test_stop_append():
    stop = Stop("1234")
    stop.bus_list.clear()

    bus = Bus("1")
    bus.time.clear()
    bus.time.append(datetime.fromtimestamp(1237))
    bus.time.append(datetime.fromtimestamp(1236))
    stop.bus_list.append(copy.deepcopy(bus))

    bus = Bus("2")
    bus.time.clear()
    bus.time.append(datetime.fromtimestamp(1235))
    bus.time.append(datetime.fromtimestamp(1234))
    stop.bus_list.append(copy.deepcopy(bus))

    assert len(stop.bus_list[0].time) == 2
    assert len(stop.bus_list[1].time) == 2
    assert stop.bus_list[1] == Bus(
        "2", [datetime.fromtimestamp(1235), datetime.fromtimestamp(1234)]
    )
    assert stop.bus_list[0] == Bus(
        "1", [datetime.fromtimestamp(1237), datetime.fromtimestamp(1236)]
    )
