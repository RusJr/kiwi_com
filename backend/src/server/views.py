import falcon
from falcon import Request, Response

import conf
from server.templates import TABLE_TEMPLATE, CHART_TEMPLATE
from storage.redis_storage import RedisStorage


REDIS = RedisStorage(host=conf.REDIS_HOST, port=conf.REDIS_PORT, db=conf.REDIS_DB)  # Do not do like that


def handle_404(req, resp):
    resp.status = falcon.HTTP_404
    resp.content_type = 'text/html'
    resp.body = "<style>body{background: url(https://pp.userapi.com/c639617/v639617533/52128/mWqvjSOe0mw.jpg) " \
                "no-repeat center center fixed; background-size: cover;}</style>"


class DirectionList:

    def on_get(self, req: Request, resp: Response):
        calendars = REDIS.list_all_calendars()
        calendars = [c.to_dict() for c in calendars]

        content = TABLE_TEMPLATE.render(calendars=calendars)
        resp.body = content
        resp.content_type = 'text/html'


class LowestPrices:

    def on_get(self, req: Request, resp: Response):
        fly_from = req.params.get('fly_from')
        fly_to = req.params.get('fly_to')

        if not fly_from or not fly_to:
            resp.status = '400'
            resp.body = 'Set "fly_from" and "fly_to"'
            return

        calendar = REDIS.get_calendar(fly_from, fly_to)
        if not calendar:
            resp.status = '404'
            resp.body = 'calendar not found'
            return

        chart_labels = [x.departure_time.strftime('%d.%m.%y') for x in calendar.flights]
        chart_prices = [x.price for x in calendar.flights]

        content = CHART_TEMPLATE.render(chart_labels=chart_labels,
                                        chart_prices=chart_prices,
                                        calendar=calendar)
        resp.body = content
        resp.content_type = 'text/html'
