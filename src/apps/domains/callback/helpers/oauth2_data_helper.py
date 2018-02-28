from apps.domains.callback.dtos import OAuth2Data


class OAuth2PersistentHelper:
    STATE_KEY = 'oauth2.state'
    CLIENT_ID_KEY = 'oauth2.client_id'
    REDIRECT_URI_KEY = 'oauth2.redirect_uri'

    @classmethod
    def set(cls, session, oauth2_data: OAuth2Data) -> None:
        session[cls.STATE_KEY] = oauth2_data.state
        session[cls.CLIENT_ID_KEY] = oauth2_data.client_id
        session[cls.REDIRECT_URI_KEY] = oauth2_data.redirect_uri

    @classmethod
    def get(cls, session) -> OAuth2Data:
        return OAuth2Data(
            session.get(cls.STATE_KEY, None),
            session.get(cls.CLIENT_ID_KEY, None),
            session.get(cls.REDIRECT_URI_KEY, None),
        )
