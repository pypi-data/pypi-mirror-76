
try:
    import logging
    import os
    import csv
    from zcrmsdk.src.com.zoho.api.authenticator.store.token_store import TokenStore
    from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
    from ....crm.api.util.constants import Constants
    from ...exception.sdk_exception import SDKException

except Exception as e:
    import logging
    import os
    import csv
    from .token_store import TokenStore
    from ..oauth_token import OAuthToken
    from ....crm.api.util.constants import Constants
    from ...exception.sdk_exception import SDKException


class FileStore(TokenStore):

    """
    This class to store user token details to the file.
    """

    logger = logging.getLogger('SDKLogger')

    def __init__(self, file_path):

        """
        Creates an FileStore class instance with the specified parameters.
        :param file_path: A str containing the token store file path.
        """
        self.file_path = file_path

        if (os.path.exists(file_path) and os.stat(file_path).st_size == 0) or not os.path.exists(file_path):
            with open(self.file_path, mode='w') as token_file:
                csv_writer = csv.writer(token_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([Constants.USER_MAIL, Constants.CLIENT_ID, Constants.REFRESH_TOKEN, Constants.ACCESS_TOKEN, Constants.GRANT_TOKEN, Constants.EXPIRY_TIME])

    def get_token(self, user, token):

        try:
            if isinstance(token, OAuthToken):
                with open(self.file_path, mode='r') as f:
                    data = csv.reader(f, delimiter=',')

                    for next_record in data:
                        if self.check_token_exists(user, token, next_record):
                            token.access_token = next_record[3]
                            token.expires_in = next_record[5]
                            token.refresh_token = next_record[2]
                            return token

        except IOError as ex:
            FileStore.logger.error(Constants.GET_TOKEN_FILE_ERROR, ex, exc_info=1)
            raise SDKException(Constants.TOKEN_STORE, Constants.GET_TOKEN_FILE_ERROR, None, cause=ex)

        return None

    def save_token(self, user, token):
        if isinstance(token, OAuthToken):
            self.delete_token(user, token)

            try:
                with open(self.file_path, mode='a+') as f:
                    csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow([user.email, token.client_id, token.refresh_token, token.access_token, token.grant_token, token.expires_in])

            except IOError as ex:
                FileStore.logger.error(Constants.SAVE_TOKEN_FILE_ERROR, ex, exc_info=1)
                raise SDKException(Constants.TOKEN_STORE, Constants.SAVE_TOKEN_FILE_ERROR, None, cause=ex)

    def delete_token(self, user, token):
        lines = list()

        if isinstance(token, OAuthToken):
            try:
                with open(self.file_path, mode='r') as f:
                    data = csv.reader(f, delimiter=',')
                    for next_record in data:
                        lines.append(next_record)
                        if self.check_token_exists(user, token, next_record):
                            lines.remove(next_record)

                with open(self.file_path, mode='w') as f:
                    csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerows(lines)

            except IOError as ex:
                FileStore.logger.error(Constants.DELETE_TOKEN_FILE_ERROR, ex, exc_info=1)
                raise SDKException(Constants.TOKEN_STORE, Constants.DELETE_TOKEN_FILE_ERROR, None, cause=ex)
    
    def check_token_exists(self, user, token, row):
        client_id = token.client_id
        email = user.email
        grant_token = token.grant_token
        refresh_token = token.refresh_token
        token_check = grant_token == row[4] if grant_token is not None else refresh_token == row[2]

        if row[0] == email and row[1] == client_id and token_check:
            return True
        
        return False

