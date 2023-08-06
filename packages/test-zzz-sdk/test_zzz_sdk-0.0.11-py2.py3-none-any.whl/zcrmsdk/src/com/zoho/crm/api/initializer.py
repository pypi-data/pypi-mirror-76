
try:

    import logging

    import os

    import json

    import traceback

    import threading

    from zcrmsdk.src.com.zoho.api.authenticator.store.token_store import TokenStore

    from zcrmsdk.src.com.zoho.api.exception.sdk_exception import SDKException

    from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature

    from zcrmsdk.src.com.zoho.crm.api.dc.data_center import DataCenter

    from zcrmsdk.src.com.zoho.crm.api.util.constants import Constants

except Exception:

    import logging

    import os

    import json

    import traceback

    import threading

    from ...api.authenticator.store.token_store import TokenStore

    from ...api.exception.sdk_exception import SDKException

    from ..api.user_signature import UserSignature

    from ..api.dc.data_center import DataCenter

    from ..api.util.constants import Constants


class Initializer(object):

    """
    This class to initialize Zoho CRM SDK.
    """

    logger = logging.getLogger('SDKLogger')

    json_details = None

    environment = None

    user = None

    store = None

    token = None

    auto_refresh_fields = None

    resource_path = None

    initializer = None

    LOCAL = threading.local()

    LOCAL.init = None

    @classmethod
    def initialize(cls, user, environment, token, store, logger, auto_refresh_fields, resource_path):

        """
        This to initialize the SDK.
        :param user: A UserSignature class instance represents the CRM user.
        :param environment: A Environment class instance containing the CRM API base URL and Accounts URL.
        :param token: A Token class instance containing the OAuth client application information.
        :param store: A TokenStore class instance containing the token store information.
        :param logger: A Logger class instance containing the log file path and Logger type.
        :param auto_refresh_fields: A Boolean value to allow or prevent auto-refreshing of the modules' fields in the background.
        :param resource_path: A String containing the absolute directory path to store user specific JSON files containing module fields information.
        """

        error = {}

        try:

            from .logger import Logger, SDKLogger

        except Exception:

            from zcrmsdk.src.com.zoho.crm.api.logger import Logger, SDKLogger

        if logger is not None:

            SDKLogger.initialize(logger.level, logger.file_path)

        else:

            SDKLogger.initialize(Logger.Levels.INFO, os.path.join(os.getcwd(), Constants.LOGFILE_NAME))

        try:

            from zcrmsdk.src.com.zoho.api.authenticator.token import Token

            if not isinstance(user, UserSignature):

                error[Constants.FIELD] = Constants.USER

                error[Constants.EXPECTED_TYPE] = UserSignature.__name__

                raise SDKException(Constants.INITIALIZATION_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            if not isinstance(environment, DataCenter.Environment):

                error[Constants.FIELD] = Constants.ENVIRONMENT

                error[Constants.EXPECTED_TYPE] = DataCenter.Environment.__name__

                raise SDKException(Constants.INITIALIZATION_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            if not isinstance(store, TokenStore):

                error[Constants.FIELD] = Constants.STORE

                error[Constants.EXPECTED_TYPE] = TokenStore.__name__

                raise SDKException(Constants.INITIALIZATION_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            if not isinstance(token, Token):

                error[Constants.FIELD] = Constants.TOKEN

                error[Constants.EXPECTED_TYPE] = Token.__name__

                raise SDKException(Constants.INITIALIZATION_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            if resource_path is None or len(resource_path) == 0:
                exception = SDKException(Constants.RESOURCE_PATH_ERROR, Constants.RESOURCE_PATH_ERROR_MESSAGE)
                # logging.getLogger('SDKLogger').info(exception.__str__())
                raise exception

            cls.environment = environment

            cls.user = user

            cls.token = token

            cls.store = store

            cls.auto_refresh_fields = auto_refresh_fields

            cls.resource_path = resource_path

            cls.initializer = cls

            logging.getLogger('SDKLogger').info(Constants.INITIALIZATION_SUCCESSFUL + cls.__str__())

        except SDKException as e:

            logging.getLogger('SDKLogger').error(Constants.INITIALIZATION_ERROR + e.__str__())

            raise e

        dir_name = os.path.dirname(__file__)

        filename = os.path.join(dir_name, '..', '..', '..', '..', Constants.JSON_DETAILS_FILE_PATH)

        with open(filename, mode='r') as JSON:

            cls.json_details = json.load(JSON)

    @classmethod
    def __str__(cls):
        return Constants.FOR_EMAIL_ID + cls.get_initializer().user.email + Constants.IN_ENVIRONMENT + cls.get_initializer().environment.url + '.'

    @classmethod
    def get_initializer(cls):

        """
        This method to get Initializer class instance.
        :return: A Initializer class instance representing the SDK configuration details.
        """

        if Initializer.LOCAL.init is not None:
            return Initializer.LOCAL.init

        return cls.initializer

    @staticmethod
    def get_json(file_path):
        with open(file_path, mode="r") as JSON:
            file_contents = json.load(JSON)
            JSON.close()

        return file_contents

    @classmethod
    def switch_user(cls, user, environment, token, auto_refresh_fields):

        """
        This method to switch the different user in SDK environment.
        :param user: A UserSignature class instance represents the CRM user.
        :param environment: A Environment class instance containing the CRM API base URL and Accounts URL.
        :param token: A Token class instance containing the OAuth client application information.
        :param auto_refresh_fields: A Boolean value to allow or prevent auto-refreshing of the modules' fields in the background.
        """

        cls.user = user

        cls.environment = environment

        cls.token = token

        cls.auto_refresh_fields = auto_refresh_fields

        cls.store = Initializer.initializer.store

        cls.resource_path = Initializer.initializer.resource_path

        Initializer.LOCAL.init = cls

        logging.getLogger('SDKLogger').info(Constants.INITIALIZATION_SWITCHED + cls.__str__())

