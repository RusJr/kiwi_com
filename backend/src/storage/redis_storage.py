import json
import logging
from typing import Any, Optional, List

import redis

from storage.interface import Storage
from storage.models import LowestPricesCalendar


logger = logging.getLogger('main_logger')


class RedisStorage(Storage):

    def __init__(self, host='localhost', port=6379, db=0, password=None) -> None:
        self._redis = redis.Redis(host, port, db, password)

    def save_calendar(self, calendar: LowestPricesCalendar) -> None:
        key = self._build_key(calendar.fly_from, calendar.fly_to)
        value = calendar.to_json()
        self._redis.set(key, value)

    def get_calendar(self, fly_from: str, fly_to: str) -> Optional[LowestPricesCalendar]:
        key = self._build_key(fly_from, fly_to)
        data = self._get(key)
        if data:
            calendar = LowestPricesCalendar.from_dict(data)
            return calendar
        else:
            return None

    def list_all_calendars(self,) -> List[LowestPricesCalendar]:
        cursor, keys = self._redis.scan()
        data = self._redis.mget(keys)

        result = []
        for row in data:
            try:
                result.append(LowestPricesCalendar.from_dict(json.loads(row)))
            except KeyError as e:
                logger.error('KeyError(%s)', e)
        return result

    def _get(self, key: str) -> Any:
        bytes_value = self._redis.get(key)
        if bytes_value:
            return json.loads(bytes_value)
        else:
            return None

    def _build_key(self, fly_from, fly_to) -> str:
        return f'{fly_from}-{fly_to}'
