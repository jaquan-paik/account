from django.test import TestCase

from lib.utils.string import generate_random_str
from lib.utils.url import is_same_url, generate_query_url


class StringTestCase(TestCase):

    def test_compare_simple_urls(self):
        url = 'https://account.ridibooks.com/ridi/callback?a=123&b=2'
        different_order_param_url = 'https://account.ridibooks.com/ridi/callback?b=2&a=123'

        different_param_url = 'https://account.ridibooks.com/ridi/callback?a=321&b=2'
        different_path_url = 'https://account.ridibooks.com/ridi/complete?a=123&b=2'

        self.assertTrue(is_same_url(url, different_order_param_url))
        self.assertFalse(is_same_url(url, different_param_url))
        self.assertFalse(is_same_url(url, different_path_url))

    def test_compare_complex_url(self):  # query 안에 url이 있고, 그 url 안에 query가 또 있는 경우.
        base_url_path = 'https://account.ridibooks.com/ridi/callback/'
        first_random_str = generate_random_str(30)
        second_random_str = generate_random_str(30)
        random_str = generate_random_str(30)

        query_url = generate_query_url(base_url_path, {'a': first_random_str, 'b': second_random_str})
        different_order_query_url = generate_query_url(base_url_path, {'b': second_random_str, 'a': first_random_str})

        url = generate_query_url(base_url_path, {'a': query_url, 'b': random_str})

        different_order_query_url = generate_query_url(base_url_path, {'a': different_order_query_url, 'b': random_str})

        different_param_url = generate_query_url(
            base_url_path, {'a': query_url, 'b': random_str, 'c': generate_random_str(30)}
        )
        self.assertTrue(is_same_url(query_url, different_order_query_url))
        self.assertTrue(is_same_url(url, different_order_query_url))
        self.assertFalse(is_same_url(url, different_param_url))
