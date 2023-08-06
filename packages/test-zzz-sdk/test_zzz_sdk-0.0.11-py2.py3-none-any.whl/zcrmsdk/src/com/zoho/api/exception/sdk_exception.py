import json


class SDKException(Exception):

    """
    This class is the common SDKException object. This stands as a POJO for the SDKException thrown.
    """

    message = 'Caused By: {code} - {message}'

    def __init__(self, code, message, details=None, cause=None):

        """
        Creates an SDKException class instance with the specified parameters.
        :param code: A str containing the Exception error code.
        :param message: A str containing the Exception error message.
        :param details: A JSON Object containing the error response.
        :param cause: A Exception class instance.
        """

        self.code = code
        self.cause = cause
        self.details = details
        self.error_message = "" if message is None else message

        if self.details is not None:
            self.error_message = self.error_message + json.dumps(self.details)

        if self.cause is not None:
            self.error_message = self.error_message + str(self.cause)

        Exception.__init__(self, code, message)

    def __str__(self):
        return self.message.format(code=self.code, message=self.error_message)
