__all__ = ['HttpCacheControlMixin']


class HttpCacheControlMixin:
    http_cache_control_max_age = None

    def get_http_cache_control_max_age(self):
        return self.http_cache_control_max_age

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        if response.status_code in [200, 304]:
            max_age = self.get_http_cache_control_max_age()
            if max_age:
                response['Cache-Control'] = 'max-age=%s' % max_age
        return response
