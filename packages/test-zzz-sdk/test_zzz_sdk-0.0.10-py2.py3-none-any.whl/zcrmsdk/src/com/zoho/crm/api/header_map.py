try:
    from zcrmsdk.src.com.zoho.crm.api.util.header_param_validator import HeaderParamValidator
except Exception:
    from .util import HeaderParamValidator


class HeaderMap(object):

    """
    This class representing the HTTP header name and value.
    """

    def __init__(self):
        """Creates an instance of HeaderMap Class"""

        self.header_map = dict()

    def add(self, header, value):

        """
        This method to add header name and value.
        :param header: A Header class instance.
        :param value: A object containing the header value.
        """

        name = header.name

        class_name = header.class_name

        if class_name is not None:
            value = HeaderParamValidator().validate(header, value)

        if name not in self.header_map:
            self.header_map[name] = str(value)
        else:
            header_value = self.header_map[name]

            self.header_map[name] = header_value + ',' + str(value)
