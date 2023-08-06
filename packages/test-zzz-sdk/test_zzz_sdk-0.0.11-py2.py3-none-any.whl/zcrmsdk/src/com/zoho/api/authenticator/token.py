
try:
    from abc import abstractmethod, ABC
    import sys

except Exception as e:
    from abc import ABCMeta, abstractmethod
    import sys

if sys.version_info[0] < 3:

    class Token:

        """
        This class to verify and set access token to APIHTTPConnector header.
        """

        __metaclass__ = ABCMeta

        @abstractmethod
        def authenticate(self, url_connection):

            """
            This method to set access token to APIHTTPConnector header.
            :param url_connection: A APIHTTPConnector class instance.
            """

            pass

else:

    class Token(ABC):

        """
        This class to verify and set access token to APIHTTPConnector header.
        """

        @abstractmethod
        def authenticate(self, url_connection):

            """
            This method to set access token to APIHTTPConnector header.
            :param url_connection: A APIHTTPConnector class instance.
            """

            pass
