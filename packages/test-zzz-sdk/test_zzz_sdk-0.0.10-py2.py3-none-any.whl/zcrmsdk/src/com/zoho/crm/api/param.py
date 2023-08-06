
class Param(object):

    """
    This class representing the HTTP parameter name.
    """

    def __init__(self, name, class_name=None):

        """
        Creates an Param class instance with the specified parameter name.
        :param name: A str containing the parameter name.
        """

        self.name = name
        self.class_name = class_name
