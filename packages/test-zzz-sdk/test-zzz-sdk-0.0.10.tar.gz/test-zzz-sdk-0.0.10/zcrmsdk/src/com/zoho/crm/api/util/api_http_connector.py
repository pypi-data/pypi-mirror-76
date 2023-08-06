try:
    import requests
    import logging
    import json
    from zcrmsdk.src.com.zoho.crm.api.util.constants import Constants

except Exception:
    from .constants import Constants
    import requests
    import logging
    import json


class APIHTTPConnector(object):
    """
    This module is to make HTTP connections, trigger the requests and receive the response.
    """

    def __init__(self):

        """
        Creates an APIHTTPConnector class instance with the specified parameters.
        """

        self.url = None
        self.headers = dict()
        self.request_method = None
        self.parameters = dict()
        self.request_body = None
        self.file = False
        self.content_type = None

    def __str__(self):
        request_headers = self.headers.copy()
        request_headers[Constants.AUTHORIZATION] = Constants.CANT_DISCLOSE

        return self.request_method + ' - ' + Constants.URL + ' = ' + self.url + ' , ' + Constants.HEADERS + ' = ' + json.dumps(request_headers) \
               + ' , ' + Constants.PARAMS + ' = ' + json.dumps(self.parameters) + '.'

    def is_set_content_type(self):
        for url in Constants.SET_TO_CONTENT_TYPE:
            if url in self.url:
                return True

        return False

    def fire_request(self, convert_instance):

        """
        This method makes a request to the Zoho CRM Rest API
        :param convert_instance: A Converter class instance to call appendToRequest method.
        :return: Response object or None
        """

        response = None
        logger = logging.getLogger('SDKLogger')

        if self.is_set_content_type():
            self.headers[Constants.CONTENT_TYPE_HEADER] = self.content_type

        logger.info(self.__str__())

        if self.request_method == Constants.REQUEST_METHOD_GET:
            response = requests.get(self.url, headers=self.headers, params=self.parameters, allow_redirects=False)

        elif self.request_method == Constants.REQUEST_METHOD_PUT:
            data = convert_instance.append_to_request(self, self.request_body)
            response = requests.put(self.url, data=data, params=self.parameters, headers=self.headers, allow_redirects=False)

        elif self.request_method == Constants.REQUEST_METHOD_POST:
            data = convert_instance.append_to_request(self, self.request_body)

            if self.file is False:
                response = requests.post(self.url, data=data, params=self.parameters, headers=self.headers, allow_redirects=False)
            else:
                response = requests.post(self.url, files=data, headers=self.headers, allow_redirects=False, data={})

        elif self.request_method == Constants.REQUEST_METHOD_DELETE:
            response = requests.delete(self.url, headers=self.headers, params=self.parameters, allow_redirects=False)

        return response
