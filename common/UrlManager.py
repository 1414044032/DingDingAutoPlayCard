import time

from application import app


class UrlManager:
    def __init__(self):
        pass

    @staticmethod
    def build_url(path):
        return path

    @classmethod
    def static_url(cls, path):
        path = '/static' + path
        return cls.build_url(path)

    @staticmethod
    def build_image_url(path):
        app_config = app.config['APP']
        url = app_config['domain'] + app.config['UPLOAD']['prefix_url'] + path
        return url