
class ParameterMap(object):

    """
    This class representing the HTTP parameter name and value.
    """

    def __init__(self):

        self.parameter_map = dict()

    def add(self, param, value):

        """
        This method to add parameter name and value.
        :param param: A Param class instance.
        :param value: A object containing the parameter value.
        """

        name = param.name

        value_list = []

        if not self.parameter_map.__contains__(name):

            value_list.append(value)

            self.parameter_map[name] = value_list

        else:

            value_list = self.parameter_map[name]

            value_list.append(value)

            self.parameter_map[name] = value_list
