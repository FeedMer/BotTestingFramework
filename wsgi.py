from prometheus_client import make_wsgi_app


def application(environ, start_fn):
    if environ['PATH_INFO'] == '/metrics':
        metrics_app = make_wsgi_app()
        return metrics_app(environ, start_fn)
