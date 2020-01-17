import logging
from datetime import datetime
from json import JSONDecodeError

import requests

from kiwi.exceptions import KiwiError, KiwiConnectionError, KiwiInternalError


logger = logging.getLogger('main_logger')


class KiwiClient:

    BASE_URL = 'https://api.skypicker.com/'
    FLIGHTS_URL = BASE_URL + 'flights'
    CHECK_FLIGHTS_URL = BASE_URL + 'check_flights'

    REQUEST_RETRIES = 3
    REQUEST_DEFAULT_TIMEOUT = 60  # seconds

    DATE_FORMAT = '%d/%m/%Y'

    def __init__(self) -> None:
        self._session = requests.session()

    def get_flights(self, fly_from: str, fly_to: str, date_from: datetime, date_to: datetime, curr='KZT') -> list:
        # probably 240 is max result
        get_params = {
            'flyFrom': fly_from,
            'to': fly_to,
            'dateFrom': date_from.strftime(self.DATE_FORMAT),  # date in UTC
            'dateTo': date_to.strftime(self.DATE_FORMAT),
            'partner': 'picky',  # "use picky partner ID for testing" - https://docs.kiwi.com/#flights-flights-get
            'curr': curr
        }

        response = self._request(
            url=self.FLIGHTS_URL,
            params=get_params
        )
        try:
            return response['data']
        except KeyError:
            raise KiwiInternalError('no "data" field')

    def _request(self, method='GET', timeout=REQUEST_DEFAULT_TIMEOUT, **request_args) -> dict:  # not only dict actually
        error = KiwiError('set retries more than 0')
        for _ in range(self.REQUEST_RETRIES):
            try:
                response = self._session.request(method=method, timeout=timeout, **request_args)
            except requests.RequestException as e:
                logger.debug('KiwiConnectionError(%s)', type(e).__name__)
                error = KiwiConnectionError(e)
            else:
                if response.status_code != 200:
                    if response.status_code >= 500:
                        raise KiwiInternalError(response.text)
                    raise KiwiError('Status %d. Content: %s' % (response.status_code, response.text))
                try:
                    return response.json()
                except JSONDecodeError:
                    raise KiwiError('internal error. cant parse json')
        raise error


if __name__ == '__main__':
    # for dev only
    from pprint import pprint
    import conf  # logging config is there

    client = KiwiClient()
    result = client.get_flights(
        fly_from='ALA',
        fly_to='TSE',
        date_from=datetime.strptime('01/02/2020', KiwiClient.DATE_FORMAT),
        date_to=datetime.strptime('25/03/2020', KiwiClient.DATE_FORMAT)
    )
    pprint(result)
    print('Count: ', len(result))
