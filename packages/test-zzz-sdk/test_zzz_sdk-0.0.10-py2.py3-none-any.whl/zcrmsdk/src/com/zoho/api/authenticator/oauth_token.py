
try:

    import logging
    import enum
    import traceback
    import json
    import time
    import requests
    from .token import Token
    from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
    from ...crm.api.util import APIHTTPConnector
    from ..exception import SDKException
    from ...crm.api.util.constants import Constants

except Exception as e:

    import logging
    import enum
    import traceback
    import json
    import time
    import requests
    from .token import Token
    from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
    from ...crm.api.util import APIHTTPConnector
    from ..exception import SDKException
    from ...crm.api.util.constants import Constants


class TokenType(enum.Enum):
    """
    This class used to give token type.
    """

    grant = Constants.GRANT

    refresh = Constants.REFRESH


class OAuthToken(Token):

    """
    This class to get tokens and check expire time.
    """

    logger = logging.getLogger('SDKLogger')

    def __init__(self, client_id, client_secret, redirect_url, token, token_type):

        """
        Creates an OAuthToken class instance with the specified parameters.
        :param client_id: A str containing the OAuth client id.
        :param client_secret: A str containing the OAuth client secret.
        :param redirect_url: A str containing the OAuth redirect URL.
        :param token: A str containing the REFRESH/GRANT token.
        :param token_type: A class containing the given token type.
        """

        error = {}

        try:

            if not isinstance(client_id, str):
                error[Constants.FIELD] = Constants.CLIENT_ID
                error[Constants.EXPECTED_TYPE] = Constants.STRING
                error[Constants.CLASS] = OAuthToken.__name__
                raise SDKException(Constants.TOKEN_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            if not isinstance(client_secret, str):
                error[Constants.FIELD] = Constants.CLIENT_SECRET
                error[Constants.EXPECTED_TYPE] = Constants.STRING
                error[Constants.CLASS] = OAuthToken.__name__
                raise SDKException(Constants.TOKEN_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            if redirect_url is not None and not isinstance(redirect_url, str):
                error[Constants.FIELD] = Constants.REDIRECT_URL
                error[Constants.EXPECTED_TYPE] = Constants.STRING
                error[Constants.CLASS] = OAuthToken.__name__
                raise SDKException(Constants.TOKEN_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            if not isinstance(token, str):
                error[Constants.FIELD] = Constants.TOKEN
                error[Constants.EXPECTED_TYPE] = Constants.STRING
                error[Constants.CLASS] = OAuthToken.__name__
                raise SDKException(Constants.TOKEN_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            if not isinstance(token_type, TokenType):
                error[Constants.FIELD] = Constants.TOKEN_TYPE
                error[Constants.EXPECTED_TYPE] = TokenType.__members__.keys()
                error[Constants.CLASS] = OAuthToken.__name__
                raise SDKException(Constants.TOKEN_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            self.client_id = client_id
            self.client_secret = client_secret
            self.redirect_url = redirect_url
            self.grant_token = token if (token_type == TokenType.grant) else None
            self.refresh_token = token if (token_type == TokenType.refresh) else None
            self.access_token = None
            self.expires_in = None

        except SDKException as ex:
            raise ex

    def authenticate(self, url_connection):
        initializer = Initializer.get_initializer()
        store = initializer.store
        user = initializer.user

        oauth_token = store.get_token(initializer.user, self)

        if oauth_token is None:
            token = self.generate_access_token(user, store).access_token if (self.refresh_token is None) else self.refresh_access_token(user, store).access_token

        elif int(oauth_token.expires_in) - int(time.time() * 1000) < 5000:
            OAuthToken.logger.info(Constants.REFRESH_TOKEN_MESSAGE)
            token = oauth_token.refresh_access_token(user, store).access_token

        else:
            token = oauth_token.access_token

        url_connection.headers[Constants.AUTHORIZATION] = Constants.OAUTH_HEADER_PREFIX + token

    def refresh_access_token(self, user, store):
        try:
            url = Initializer.get_initializer().environment.accounts_url

            body = {
                Constants.REFRESH_TOKEN: self.refresh_token,
                Constants.CLIENT_ID: self.client_id,
                Constants.CLIENT_SECRET: self.client_secret,
                Constants.GRANT_TYPE: Constants.REFRESH_TOKEN
            }

            response = requests.post(url, data=body, params=None, headers=None, allow_redirects=False).json()
            store.save_token(user, self.parse_response(response=response))

        except SDKException as ex:
            raise ex

        except Exception as ex:
            OAuthToken.logger.error(Constants.SAVE_TOKEN_ERROR + ex.__str__())
            raise SDKException(None, None, None, cause=ex)

        return self

    def generate_access_token(self, user, store):
        try:
            url = Initializer.get_initializer().environment.accounts_url

            body = {
                Constants.GRANT_TYPE: Constants.GRANT_TYPE_AUTH_CODE,
                Constants.CLIENT_ID: self.client_id,
                Constants.CLIENT_SECRET: self.client_secret,
                Constants.REDIRECT_URL: self.redirect_url,
                Constants.CODE: self.grant_token
            }

            response = requests.post(url, data=body, params=None, headers=None, allow_redirects=True).json()
            store.save_token(user, self.parse_response(response=response))

        except SDKException as ex:
            raise ex

        except Exception as ex:
            OAuthToken.logger.error(Constants.SAVE_TOKEN_ERROR + ex.__str__())
            raise SDKException(None, None, None, cause=ex)

        return self

    def parse_response(self, response):
        response_json = dict(response)

        if not Constants.ACCESS_TOKEN in response_json:
            OAuthToken.logger.error(Constants.GET_TOKEN_ERROR)
            raise SDKException(code=Constants.INVALID_CLIENT_ERROR, message=str(response_json.get(Constants.ERROR_KEY)))

        self.access_token = response_json.get(Constants.ACCESS_TOKEN)
        self.expires_in = str(int(time.time() * 1000) + self.get_token_expires_in(response=response_json))  # expires in

        if Constants.REFRESH_TOKEN in response_json:
            self.refresh_token = response_json.get(Constants.REFRESH_TOKEN)

        return self

    def get_token_expires_in(self, response):
        return int(response[Constants.EXPIRES_IN]) if Constants.EXPIRES_IN_SEC in response else int(response[Constants.EXPIRES_IN]) * 1000
