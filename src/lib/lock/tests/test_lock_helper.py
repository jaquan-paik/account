from unittest.mock import MagicMock

from django.test import TestCase

from lib.lock.helper import LockHelper


class LockHelperTestCase(TestCase):
    def setUp(self):
        self.data = {}

        def set_key(key: str, uuid: str, ttl: str) -> bool:
            self.data[key] = uuid
            return True

        def delete_key(key: str) -> bool:
            if key not in self.data:
                return False
            del self.data[key]
            return True

        def extend_ttl(key: str, ttl: str) -> bool:
            return key in self.data

        def is_locked(key: str) -> bool:
            return key in self.data

        LockHelper.lock_manager.set_key = MagicMock(side_effect=set_key)
        LockHelper.lock_manager.delete_key = MagicMock(side_effect=delete_key)
        LockHelper.lock_manager.extend_ttl = MagicMock(side_effect=extend_ttl)
        LockHelper.lock_manager.is_locked = MagicMock(side_effect=is_locked)

    def test_lock(self):
        lock_helper = LockHelper('-----dummykey-----')

        self.assertTrue(lock_helper.lock())
        self.assertTrue(lock_helper.is_locked())
        self.assertTrue(lock_helper.ping())
        self.assertTrue(lock_helper.unlock())

        self.assertFalse(lock_helper.is_locked())

    def test_lock_multi(self):
        lock_helper_one = LockHelper('-----dummykey-----')
        lock_helper_two = LockHelper('-----dummykey-----')

        self.assertTrue(lock_helper_one.lock())
        self.assertTrue(lock_helper_two.is_locked())
        self.assertTrue(lock_helper_one.unlock())
        self.assertFalse(lock_helper_two.is_locked())

    def test_unlock(self):
        lock_helper = LockHelper('-----dummykey-----')

        self.assertFalse(lock_helper.unlock())

        self.assertTrue(lock_helper.lock())
        self.assertTrue(lock_helper.unlock())
