
class APIResponse(object):

    """
    This class is the common API response object.
    """

    def __init__(self, headers, status_code, object):

        """
        Creates an APIResponse class instance with the specified parameters.
        :param headers: A dict containing the API response headers.
        :param status_code: An integer containing the API response HTTP status code.
        :param object: A object containing the API response POJO class instance.
        """

        self.__headers = headers

        self.__status_code = status_code

        self.__object = object

    def get_headers(self):

        """
        This is a getter method to get API response headers.
        :return: A dict representing the API response headers.
        """

        return self.__headers

    def get_status_code(self):

        """
        This is a getter method to get the API response HTTP status code.
        :return: An integer representing the API response HTTP status code.
        """

        return self.__status_code

    def get_object(self):

        """
        This method to get an API response POJO class instance.
        :return: A class instance.
        """

        return self.__object
