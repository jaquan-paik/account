from typing import Tuple

from apps.domains.ridi.dtos import TokenData


class InHouseClientCredentialsService:
    @classmethod
    def create_token(cls, client_id: str, u_idx: int, audience: str) -> Tuple[TokenData, TokenData]:
        pass
