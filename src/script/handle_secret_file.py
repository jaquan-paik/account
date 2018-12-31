import argparse
import os
import sys


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

from lib.secret.constants import SecretEnvironment  # flake8: noqa: E402 # pylint:disable=wrong-import-position
from lib.secret.secret import SecretFileGenerator, SecretFileConverter  # flake8: noqa: E402 # pylint:disable=wrong-import-position

args_parser = argparse.ArgumentParser()
args_parser.add_argument('-a', '--action', help='generate or encrypt')
args_parser.add_argument('-e', '--environment', required=False, help='environment (development or staging or production)')
args = args_parser.parse_args()

if args.action == 'generate':
    secret_env = SecretEnvironment.to_string(args.environment)

    secrets_generator = SecretFileGenerator()
    secrets_generator.generate(secret_env)

elif args.action == 'encrypt':
    secret_file_handler = SecretFileConverter()
    secret_file_handler.convert_to_encrypted_file()

else:
    args_parser.print_help()
