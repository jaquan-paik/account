import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

from lib.secret.secret import SecretFileGenerator, SecretFileConverter, ENV_PROD, ENV_DEV  # flake8: noqa: E402

args_parser = argparse.ArgumentParser()
args_parser.add_argument('action', help='generate_dev / generate_prod / encrypt')
args = args_parser.parse_args()

if args.action == 'generate_production':
    secrets_generator = SecretFileGenerator()
    secrets_generator.generate(ENV_PROD)
elif args.action == 'generate_development':
    secrets_generator = SecretFileGenerator()
    secrets_generator.generate(ENV_DEV)
elif args.action == 'encrypt':
    secret_file_handler = SecretFileConverter()
    secret_file_handler.convert_to_encrypted_file()
else:
    args_parser.print_help()
