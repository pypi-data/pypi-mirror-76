
try:
    from abc import ABC, abstractmethod
    import sys

except Exception as e:
    from abc import ABCMeta, abstractmethod
    import sys

if sys.version > '3':

    class TokenStore(ABC):

        """
        This class to store user token details.
        """

        @abstractmethod
        def get_token(self, user, token):

            """
            This method to get user token details.
            :param user: A UserSignature class instance.
            :param token:A Token class instance.
            :return: A Token class instance representing the user token details.
            """

            pass

        @abstractmethod
        def save_token(self, user, token):

            """
            This method to store user token details.
            :param user: A UserSignature class instance.
            :param token: A Token class instance.
            """

            pass

        @abstractmethod
        def delete_token(self, user, token):

            """
            This method to delete user token details.
            :param user: A UserSignature class instance.
            :param token: A Token class instance.
            """

            pass

else:

    class TokenStore:

        """
        This class to store user token details.
        """

        __metaclass__ = ABCMeta

        @abstractmethod
        def get_token(self, user, token):

            """
            This method to get user token details.
            :param user: A UserSignature class instance.
            :param token:A Token class instance.
            :return: A Token class instance representing the user token details.
            """

            pass

        @abstractmethod
        def save_token(self, user, token):

            """
            This method to store user token details.
            :param user: A UserSignature class instance.
            :param
            """

            pass

        @abstractmethod
        def delete_token(self, user, token):
            """
            This method to delete user token details.
            :param user: A UserSignature class instance.
            :param token: A Token class instance.
            """

            pass
