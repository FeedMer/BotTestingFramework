from prometheus_client import make_wsgi_app
from main import metrics_app


def application(environ, start_fn):
    if environ['PATH_INFO'] == '/metrics':
        return metrics_app(environ, start_fn)
