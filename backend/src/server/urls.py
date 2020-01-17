import falcon

from server.views import handle_404, LowestPrices, DirectionList

app = falcon.API()


app.add_route('/', DirectionList())
app.add_route('/lowest_prices', LowestPrices())

# add default 404
app.add_sink(handle_404, '')
