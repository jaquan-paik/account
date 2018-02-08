from django.test import TestCase

from lib.utils.string import is_include_emoji, is_last_char_has_batchim


class StringTestCase(TestCase):
    def setUp(self):
        pass

    def test_emoji_test(self):
        emoji_string = '😁😂this is emoji string'
        not_emoji_string = 'this is not emoji string'

        self.assertTrue(is_include_emoji(emoji_string))
        self.assertFalse(is_include_emoji(not_emoji_string))

    def test_batchim_test(self):
        batchim = '받침'
        not_batchim = '받치'
        two_not_batchim = '바치'
        not_batchim2 = '바침'

        self.assertTrue(is_last_char_has_batchim(batchim))
        self.assertFalse(is_last_char_has_batchim(not_batchim))
        self.assertFalse(is_last_char_has_batchim(two_not_batchim))
        self.assertTrue(is_last_char_has_batchim(not_batchim2))
