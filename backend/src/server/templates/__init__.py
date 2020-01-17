import os
import jinja2


def load_template(name):
    path = os.path.join('server', 'templates', name)
    path = os.path.abspath(path)
    try:
        with open(path, 'r') as fp:
            return jinja2.Template(fp.read())
    except FileNotFoundError:
        path = os.path.join('src', 'server', 'templates', name)
        path = os.path.abspath(path)
        with open(path, 'r') as fp:
            return jinja2.Template(fp.read())


CHART_TEMPLATE = load_template('chart.html')
TABLE_TEMPLATE = load_template('table.html')
