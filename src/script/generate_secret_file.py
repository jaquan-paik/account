import sys

import argparse
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))


def run():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-e', '--environment', required=True, help='environment (local or development, staging, production)')
    args_parser.add_argument('-p', '--path', required=False, help='if environment is local, raw secret file path is required.')
    args = args_parser.parse_args()

    from lib.secret.secret_file_generator import RawSecretFileLoader, RawSecretParameterStoreLoader
    from lib.secret.secret_file_generator import SecretFileGenerator
    from infra.configure.constants import SecretKeyName

    if args.environment == 'local':
        raw_secret_loader = RawSecretFileLoader(args.path, SecretKeyName.get_list())

    else:
        raw_secret_loader = RawSecretParameterStoreLoader(args.environment, SecretKeyName.get_list())

    SecretFileGenerator.generate(raw_secret_loader)

    return 0


def main():
    sys.exit(run())


if __name__ == "__main__":
    main()
