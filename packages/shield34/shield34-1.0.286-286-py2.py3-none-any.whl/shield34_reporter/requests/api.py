import requests
from shield34_reporter.utils.external_proxy import get_external_proxies


def request(method, url, **kwargs):
    response = requests.request(method=method,
                                url=url,
                                **kwargs)
    return response


def get(url, params=None, **kwargs):
    response = requests.get(url=url,
                            params=params,
                            **kwargs)
    return response


def post(url, data=None, json=None, **kwargs):
    response = requests.post(url=url,
                             data=data,
                             json=json,
                             **kwargs)
    return response


def options(url, **kwargs):
    response = requests.options(url, proxies=get_external_proxies(), **kwargs)
    return response


def head(url, **kwargs):
    response = requests.head(url, proxies=get_external_proxies(), **kwargs)
    return response


def put(url, data=None, **kwargs):
    response = requests.put(url=url,
                            data=data,
                            **kwargs)
    return response


def patch(url, data=None, **kwargs):
    return requests.patch(url, data=data, proxies=get_external_proxies(), **kwargs)


def delete(url, **kwargs):
    return requests.delete(url, proxies=get_external_proxies(), **kwargs)


def get_arg(name, default_value, **kwargs):
    if name in kwargs:
        return kwargs.get(name)
    else:
        return default_value
