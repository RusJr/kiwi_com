from typing import List, Any, Optional

from storage.models import LowestPricesCalendar


class Storage:  # interface)

    def save_calendar(self, calendar: LowestPricesCalendar) -> None:
        raise NotImplementedError

    def get_calendar(self, fly_from: str, fly_to: str) -> Optional[LowestPricesCalendar]:
        raise NotImplementedError

    def list_all_calendars(self,) -> List[LowestPricesCalendar]:
        raise NotImplementedError
