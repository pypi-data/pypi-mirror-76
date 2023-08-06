
class Header(object):

    """
    This class representing the HTTP header name.
    """

    def __init__(self, name, class_name=None):

        """
        Creates an Header class instance with the specified header name.
        :param name: A str containing the header name.
        """

        self.name = name
        self.class_name = class_name
