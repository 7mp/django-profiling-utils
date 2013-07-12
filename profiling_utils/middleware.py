# -*- coding: utf-8 -*-
import logging
import time

logger = logging.getLogger(__name__)

def create_shared_dict(**kwargs):
    """
    Prepare a shared dict for middlewares

    Key ``ignores`` contains boolean tests for request-checking;
    if any(test_in_ignores(request)), request is ignored.
    """
    def is_media(request):
        from django.conf import settings
        return request.path_info.startswith(settings.MEDIA_URL)

    shared_dict = {'ignores': [lambda request: is_media(request)]}
    shared_dict.update(**kwargs)
    return shared_dict

# TODO: We could skip this whole thing e.g. with a meta class solution. Later.
request_queries_shared_dict = create_shared_dict(query_count={})
class RequestQueryCounterMiddleware(object):
    def __init__(self):
        self.__dict__ = request_queries_shared_dict

    def process_request(self, request):
        if not any(ignore_test(request) for ignore_test in self.ignores):
            from django.db import connection
            self.query_count[id(request)] = len(connection.queries)
        return None

    def process_response(self, request, response):
        if not any(ignore_test(request) for ignore_test in self.ignores):
            from django.db import connection
            query_count = len(connection.queries) - self.query_count[id(request)]
            logger.debug('Queries for request #%s (%s %s): %d' % (id(request), request.method, request.path_info, query_count))
        return response

durations_shared_dict = create_shared_dict(durations={})
class RequestDurationMiddleware(object):
    def __init__(self):
        self.__dict__ = durations_shared_dict

    def process_request(self, request):
        if not any(ignore_test(request) for ignore_test in self.ignores):
            from django.db import connection
            self.durations[id(request)] = time.time()
        return None

    def process_response(self, request, response):
        if not any(ignore_test(request) for ignore_test in self.ignores):
            duration = (time.time() - self.durations[id(request)]) * 1000 # in ms
            logger.debug('Duration for request #%s (%s %s): %.3f ms' % (id(request), request.method, request.path_info, duration))
        return response
