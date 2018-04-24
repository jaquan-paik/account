

def make_auth_data_key(issuer: str, subject: str) -> str:
    return f'{issuer}-{subject}'
