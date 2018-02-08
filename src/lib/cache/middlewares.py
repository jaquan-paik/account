from django.middleware.cache import CacheMiddleware


class DynamicKeyPrefixCacheMiddleware(CacheMiddleware):
    def __init__(self, *args, **kwargs):
        super(DynamicKeyPrefixCacheMiddleware, self).__init__(*args, **kwargs)
        self.get_key_prefix = kwargs['get_key_prefix']
        self.key_prefix = None

    def process_request(self, request):
        self.key_prefix = self.get_key_prefix(request)
        return super(DynamicKeyPrefixCacheMiddleware, self).process_request(request)

    def process_response(self, request, response):
        self.key_prefix = self.get_key_prefix(request)
        return super(DynamicKeyPrefixCacheMiddleware, self).process_response(request, response)
