import json

from django.test import TestCase

from lib.crypto.encrypt import CryptoHelper
from lib.secret.secret import CRYPTO_KEY, SecretFileGenerator


class SecretFileGeneratorTestCase(TestCase):
    def test_encrypt(self):
        secret_generator = SecretFileGenerator()
        encrypted = secret_generator.encrypt_secrets({
            'test_key': 'test_value'
        })

        decrypted = CryptoHelper(CRYPTO_KEY).decrypt(encrypted)
        decrypted_secrets = json.loads(decrypted)

        self.assertEqual(decrypted_secrets['test_key'], 'test_value')
