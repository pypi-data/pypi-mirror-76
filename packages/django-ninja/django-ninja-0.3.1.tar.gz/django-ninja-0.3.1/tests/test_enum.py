from datetime import date
from enum import Enum
from json import encoder
from pydantic import BaseModel
from ninja import NinjaAPI
from client import NinjaClient


class RoomEnum(str, Enum):
    double = "double"
    twin = "twin"
    single = "single"


class Booking(BaseModel):
    start: date
    end: date
    room: RoomEnum = RoomEnum.double


api = NinjaAPI()


@api.get("/bookings")
def get_bookings(request, room: RoomEnum):
    return room.value


@api.post("/book")
def create_booking(request, booking: Booking):
    return booking


@api.get("/search")
def booking_search(request, date: date, room: RoomEnum):
    return {"date": date, "room": room}


client = NinjaClient(api)


def test_enums():
    response = client.post(
        "/book", json={"start": "2020-01-01", "end": "2020-01-02", "room": "double"}
    )
    assert response.status_code == 200, response.content
    assert response.json() == {
        "start": "2020-01-01",
        "end": "2020-01-02",
        "room": "double",
    }

    response = client.post(
        "/book", json={"start": "2020-01-01", "end": "2020-01-02", "room": "triple"}
    )
    assert response.status_code == 422

    response = client.get("/search?date=2020-01-01&room=twin")
    assert response.status_code == 200
    assert response.json() == {
        "date": "2020-01-01",
        "room": "twin",
    }

    response = client.get("/search?date=2020-01-01&room=other")
    assert response.status_code == 422


def test_schema():
    schema = api.get_openapi_schema()
    from pprint import pprint
    import json
    from ninja.responses import NinjaJSONEncoder

    schema_json = json.dumps(schema, cls=NinjaJSONEncoder, indent=1)

    print(schema_json)
    # assert False
