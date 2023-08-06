
import logging

import re

import traceback

from zcrmsdk.src.com.zoho.api.exception import SDKException

from zcrmsdk.src.com.zoho.crm.api.util.constants import Constants


class User(object):

    """
    This class representing the CRM user email.
    """

    logger = logging.getLogger('client_lib')

    regex = Constants.EMAIL_REGEX

    def __init__(self, email):

        """
        Creates an User class instance with the specified user email.
        :param email: A str containing the CRM user email
        """

        error = {}

        try:

            if re.search(User.regex, email) is None:

                error[Constants.FIELD] = Constants.EMAIL

                error[Constants.EXPECTED_TYPE] = Constants.EMAIL

                raise SDKException(Constants.USER_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            self.email = email

        except SDKException as e:

            User.logger.error(Constants.USER_INITIALIZATION_ERROR + e.__str__())
