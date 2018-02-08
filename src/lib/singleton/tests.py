from django.test import TestCase

from lib.singleton.singleton import Singleton


class SingletonTestCase(TestCase):
    def setUp(self):
        class TestClass:
            pass

        self.klass = TestClass
        self.klassWithSingleton = Singleton(TestClass)

    def test_singleton_object(self):
        a_instance = self.klassWithSingleton()
        b_instance = self.klassWithSingleton()

        self.assertEqual(a_instance, b_instance)

    def test_not_equal_instances(self):
        a_instance = self.klass()
        b_instance = self.klassWithSingleton()

        self.assertNotEqual(a_instance, b_instance)
