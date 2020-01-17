import json
from datetime import datetime
from typing import List


class Jsonable():

    @classmethod
    def from_dict(cls, data: dict):
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError

    def to_json(self) -> str:
        raise NotImplementedError


class Flight(Jsonable):

    def __init__(self, fly_from: str, fly_to: str, price: int, departure_time: datetime, booking_token: str) -> None:
        self.fly_from = fly_from
        self.fly_to = fly_to
        self.price = price
        self.departure_time = departure_time
        self.booking_token = booking_token

    def to_dict(self) -> dict:
        return {
            'departure_time': self.departure_time,
            'fly_from': self.fly_from,
            'fly_to': self.fly_to,
            'price': self.price,
            'booking_token': self.booking_token,
        }

    def to_json(self) -> str:
        data = self.to_dict()
        data['departure_time'] = int(datetime.timestamp(self.departure_time))
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            departure_time=datetime.fromtimestamp(data['departure_time']),
            fly_from=data['fly_from'],
            fly_to=data['fly_to'],
            price=data['price'],
            booking_token=data['booking_token'],
        )

    def __str__(self) -> str:
        return f'{self.price}'


class CalendarStatuses:
    READY = 'ready'
    IN_PROCESS = 'in_process'


class LowestPricesCalendar(Jsonable):
    def __init__(self, fly_from: str, fly_to: str, status: str, progress_total: int, progress_done: int,
                 flights: List[Flight]) -> None:
        self.fly_from = fly_from
        self.fly_to = fly_to
        self.status = status
        self.progress_total = progress_total
        self.progress_done = progress_done
        self.flights = flights

    def to_dict(self) -> dict:
        return {
            'fly_from': self.fly_from,
            'fly_to': self.fly_to,
            'status': self.status,
            'progress_total': self.progress_total,
            'progress_done': self.progress_done,
            'flights': [f.to_dict() for f in self.flights],
        }

    def to_json(self) -> str:
        data = self.to_dict()
        for flight in data['flights']:
            flight['departure_time'] = int(datetime.timestamp(flight['departure_time']))
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            fly_from=data['fly_from'],
            fly_to=data['fly_to'],
            status=data['status'],
            progress_total=data['progress_total'],
            progress_done=data['progress_done'],
            flights=[Flight.from_dict(f) for f in data['flights']],
        )

    def __str__(self) -> str:
        return f'{self.fly_from}-{self.fly_to}'
