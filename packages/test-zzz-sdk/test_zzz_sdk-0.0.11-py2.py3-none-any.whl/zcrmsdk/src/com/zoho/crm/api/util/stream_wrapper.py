
import os


class StreamWrapper(object):

    """
    This class handles the file stream and name.
    """

    def __init__(self, name=None, stream=None, file_path=None):

        """
        Creates a StreamWrapper class instance with the specified parameters.
        :param name: A str containing the file name.
        :param stream: A stream containing the file stream.
        :param file_path: A str containing the absolute file path.
        """

        if file_path is not None:
            self.__name = os.path.basename(file_path)
            self.__stream = open(file_path, 'rb')

        else:
            self.__name = name
            self.__stream = stream

    def get_name(self):

        """
        This is a getter method to get the file name.
        :return: A str representing the file name.
        """

        return self.__name

    def get_stream(self):

        """
        This is a getter method to get the file input stream.
        :return: A stream representing the file input stream.
        """

        return self.__stream
