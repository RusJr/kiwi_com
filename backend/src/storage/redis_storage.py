import json
from typing import Any, Optional

import redis

from storage.interface import Storage
from storage.models import LowestPricesCalendar


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

    def _get(self, key: str) -> Any:
        bytes_value = self._redis.get(key)
        if bytes_value:
            return json.loads(bytes_value)
        else:
            return None

    def _build_key(self, fly_from, fly_to) -> str:
        return f'{fly_from}-{fly_to}'
