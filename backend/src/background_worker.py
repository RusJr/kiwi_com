import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple

from kiwi.client import KiwiClient
from storage.interface import Storage
from storage.models import Flight, LowestPricesCalendar, CalendarStatuses


logger = logging.getLogger('main_logger')


class Worker:

    def __init__(self, kiwi_client: KiwiClient, storage: Storage, days_ahead: int, top_flights: Tuple[str, str]) -> None:
        self.days_ahead = days_ahead
        self.top_flights = top_flights
        self._kiwi_client = kiwi_client
        self._storage = storage

    def run(self) -> None:
        self.init_calendars()

        one_day = timedelta(days=1)
        date = datetime.now()

        for day_number in range(1, self.days_ahead+1):
            for fly_from, fly_to in self.top_flights:
                cheapest_flight = self._get_cheapest(fly_from, fly_to, date_from=date, date_to=date)

                calendar = self._storage.get_calendar(fly_from, fly_to)
                calendar.progress_done += 1
                if day_number == self.days_ahead:
                    calendar.status = CalendarStatuses.READY
                if cheapest_flight:
                    calendar.flights.append(cheapest_flight)
                self._storage.save_calendar(calendar)

                logger.info('Day %d/%d. %s-%s. %s', day_number, self.days_ahead, fly_from, fly_to, cheapest_flight)
            date += one_day

        logger.info('Done!')

    def init_calendars(self) -> None:
        for fly_from, fly_to in self.top_flights:
            self._storage.save_calendar(LowestPricesCalendar(
                fly_from=fly_from,
                fly_to=fly_to,
                status=CalendarStatuses.IN_PROCESS,
                progress_total=self.days_ahead,
                progress_done=0,
                flights=[]
            ))

    def _get_cheapest(self, fly_from: str, fly_to: str, date_from: datetime, date_to: datetime) -> Optional[Flight]:
        day_flights = self._kiwi_client.get_flights(fly_from, fly_to, date_from, date_to)
        if not day_flights:
            return None
        lowest_price = min(f['price'] for f in day_flights)
        the_flight = next(f for f in day_flights if f['price'] == lowest_price)
        return self._parse_flight(the_flight)

    def _parse_flight(self, flight: dict) -> Flight:
        return Flight(
            departure_time=datetime.fromtimestamp(flight['dTimeUTC']),
            fly_from=flight['cityCodeFrom'],
            fly_to=flight['cityCodeTo'],
            price=flight['price'],
            booking_token=flight['booking_token'],
        )


if __name__ == '__main__':
    from time import sleep

    import schedule

    import conf
    from storage.redis_storage import RedisStorage

    kiwi_client_instance = KiwiClient()
    redis = RedisStorage(host=conf.REDIS_HOST, port=conf.REDIS_PORT, db=conf.REDIS_DB)
    worker = Worker(kiwi_client_instance, redis, conf.DAYS, conf.TOP_FLIGHTS)

    # run immediately for the first time
    worker.run()

    # ----------------------------------------------------------------
    logger.info('Task scheduled at %s', conf.UPDATE_TIME)
    schedule.every().day.at(conf.UPDATE_TIME).do(lambda: worker.run())
    while True:
        schedule.run_pending()
        sleep(1)
