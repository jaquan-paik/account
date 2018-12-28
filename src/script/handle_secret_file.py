import argparse
import os
import sys
from dotenv import dotenv_values

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

from lib.secret.constants import SecretEnvironment  # flake8: noqa: E402 # pylint:disable=wrong-import-position
from lib.secret.secret import SecretFileGenerator, SecretFileConverter  # flake8: noqa: E402 # pylint:disable=wrong-import-position
from lib.utils.file import FileHandler

args_parser = argparse.ArgumentParser()
args_parser.add_argument('-a', '--action', help='generate or encrypt')
args_parser.add_argument('-s', '--stage', required=False, help='stage (development or staging or production)')
args_parser.add_argument('-e', '--environment', required=False, action='append', help='environment variable to put in secret')
args_parser.add_argument('-ef', '--env_file', required=False, help='environment file to put in secret')
args = args_parser.parse_args()

if args.action == 'generate':
    env = {}
    if args.environment:
        env.update(dict([env.split('=') for env in args.environment]))

    if args.env_file:
        file_handler = FileHandler()
        env_file_path = file_handler.get_file_path(args.env_file)
        env.update(dotenv_values(dotenv_path=env_file_path))

    secrets_generator = SecretFileGenerator()
    stage = SecretEnvironment.to_string(args.stage)
    secrets_generator.generate(stage, env)

elif args.action == 'encrypt':
    secret_file_handler = SecretFileConverter()
    secret_file_handler.convert_to_encrypted_file()

else:
    args_parser.print_help()
