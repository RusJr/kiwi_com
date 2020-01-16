from datetime import datetime, timedelta
from typing import Optional

import conf
from kiwi.client import KiwiClient


class Worker:

    def __init__(self, kiwi_client: KiwiClient) -> None:
        self._kiwi_client = kiwi_client

    def run(self) -> None:
        one_day = timedelta(days=1)
        date = datetime.now()

        for day_number in range(conf.DAYS_AHEAD):
            for fly_from, fly_to in conf.TOP_FLIGHTS:
                cheapest_flight = self._get_cheapest(fly_from, fly_to, date_from=date, date_to=date)
                print(cheapest_flight)
            date += one_day

    def _get_cheapest(self, fly_from: str, fly_to: str, date_from: datetime, date_to: datetime) -> Optional[dict]:
        day_flights = self._kiwi_client.get_flights(fly_from, fly_to, date_from, date_to)
        if not day_flights:
            return None
        lowest_price = min(f['price'] for f in day_flights)
        the_flight = next(f for f in day_flights if f['price'] == lowest_price)
        return self._parse_flight(the_flight)

    def _parse_flight(self, flight: dict) -> dict:
        return {
            'deperture_time': datetime.fromtimestamp(flight['dTimeUTC']),
            'fly_from': flight['cityCodeFrom'],
            'fly_to': flight['cityCodeTo'],
            'price': flight['price'],
            'booking_token': flight['booking_token'],
        }


if __name__ == '__main__':
    kiwi_client_instance = KiwiClient()
    worker = Worker(kiwi_client_instance)
    worker.run()
