
try:
    import logging
    import mysql.connector
    from mysql.connector import Error
    from zcrmsdk.src.com.zoho.api.authenticator.store.token_store import TokenStore
    from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
    from zcrmsdk.src.com.zoho.crm.api.util.constants import Constants
    from zcrmsdk.src.com.zoho.api.exception.sdk_exception import SDKException

except Exception as e:
    import logging
    import mysql.connector
    from mysql.connector import Error
    from .token_store import TokenStore
    from ..oauth_token import OAuthToken
    from ....crm.api.util.constants import Constants
    from ...exception.sdk_exception import SDKException


class DBStore(TokenStore):

    """
    This class to store user token details to the MySQL DataBase.
    """

    logger = logging.getLogger('SDKLogger')

    def __init__(self, host=None, database_name=None, user_name=None, password=None, port_number=None):

        """
        Creates an DBStore class instance with the specified parameters.
        :param host: A str containing the DataBase host name. Default value is localhost
        :param database_name: A str containing the DataBase name. Default value is zohooauth
        :param user_name: A str containing the DataBase user name. Default value is root
        :param password: A str containing the DataBase password. Default value is an empty string
        :param port_number: A str containing the DataBase port number. Default value is 3306
        """

        self.host = host if host is not None else Constants.MYSQL_HOST
        self.database_name = database_name if database_name is not None else Constants.MYSQL_DATABASE_NAME
        self.user_name = user_name if user_name is not None else Constants.MYSQL_USER_NAME
        self.password = password if password is not None else ""
        self.port_number = port_number if port_number is not None else Constants.MYSQL_PORT_NUMBER

    def get_token(self, user, token):

        try:

            # connection = mysql.connector.connect(host=self.host, database=self.database_name, user=self.user_name, \
            #                                      password=self.password, auth_plugin='')

            connection = mysql.connector.connect(host=self.host, database=self.database_name, user=self.user_name, \
                                                 password=self.password, port= self.port_number)
            try:
                if isinstance(token, OAuthToken):
                    cursor = connection.cursor()
                    query = self.construct_dbquery(user, token, False)
                    cursor.execute(query)
                    result = cursor.fetchone()

                    if result is not None:
                        token.access_token = result[4]
                        token.expires_in = result[6]
                        token.refresh_token = result[3]

                        return token

            except Error as ex:
                raise ex

            finally:
                cursor.close()
                connection.close()

        except Error as ex:
            DBStore.logger.error(Constants.GET_TOKEN_DB_ERROR + str(ex))
            raise SDKException(Constants.TOKEN_STORE, Constants.GET_TOKEN_DB_ERROR, None, cause=ex)

        return None

    def save_token(self, user, token):
        self.delete_token(user, token)

        try:
            connection = mysql.connector.connect(host=self.host, database=self.database_name, user=self.user_name, password=self.password, port=self.port_number)

            try:
                if isinstance(token, OAuthToken):
                    cursor = connection.cursor()
                    query = "insert into oauthtoken (user_mail,client_id,refresh_token,access_token,grant_token,expiry_time) values (%s,%s,%s,%s,%s,%s);"
                    val = (user.email, token.client_id, token.refresh_token, token.access_token, token.grant_token, token.expires_in)
                    cursor.execute(query, val)
                    connection.commit()

            except Error as ex:
                raise ex

            finally:
                cursor.close()
                connection.close()

        except Error as ex:
            DBStore.logger.error(Constants.SAVE_TOKEN_DB_ERROR + str(ex))
            raise SDKException(Constants.TOKEN_STORE, Constants.SAVE_TOKEN_DB_ERROR, None, cause=ex)

    def delete_token(self, user, token):
        try:
            connection = mysql.connector.connect(host=self.host, database=self.database_name, user=self.user_name, password=self.password, port=self.port_number)

            try:
                if isinstance(token, OAuthToken):
                    cursor = connection.cursor()
                    query = self.construct_dbquery(user, token, True)
                    cursor.execute(query)
                    connection.commit()

            except Error as ex:
                raise ex

            finally:
                cursor.close()
                connection.close()

        except Error as ex:
            DBStore.logger.error(Constants.DELETE_TOKEN_DB_ERROR, ex)
            raise SDKException(Constants.TOKEN_STORE, Constants.DELETE_TOKEN_DB_ERROR, None, cause=ex)

    def construct_dbquery(self, user, token, is_delete):
        query = "delete from " if is_delete is True else "select * from "
        query += "oauthtoken " + "where user_mail ='" + user.email + "' and client_id='" + token.client_id + "' and "

        if token.grant_token is not None:
            query += "grant_token='" + token.grant_token + "'"

        else:
            query += "refresh_token='" + token.refresh_token + "'"

        return query
