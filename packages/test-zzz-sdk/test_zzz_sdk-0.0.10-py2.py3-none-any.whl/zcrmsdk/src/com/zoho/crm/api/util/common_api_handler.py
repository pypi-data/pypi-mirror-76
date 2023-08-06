
try:
    import json
    import platform
    import urllib
    from zcrmsdk.src.com.zoho.crm.api.util.api_http_connector import APIHTTPConnector
    from zcrmsdk.src.com.zoho.crm.api.util.json_converter import JSONConverter
    from zcrmsdk.src.com.zoho.crm.api.util.xml_converter import XMLConverter
    from zcrmsdk.src.com.zoho.crm.api.util.form_data_converter import FormDataConverter
    from zcrmsdk.src.com.zoho.crm.api.util.downloader import Downloader
    from zcrmsdk.src.com.zoho.crm.api.util.constants import Constants
    from zcrmsdk.src.com.zoho.crm.api.util.api_response import APIResponse
    from zcrmsdk.src.com.zoho.crm.api.header_map import HeaderMap
    from zcrmsdk.src.com.zoho.crm.api.header import Header
    from zcrmsdk.src.com.zoho.crm.api.parameter_map import ParameterMap
    from zcrmsdk.src.com.zoho.crm.api.param import Param
    from zcrmsdk.src.com.zoho.api.exception import SDKException

except Exception:
    import json
    import platform
    import urllib
    from .api_http_connector import APIHTTPConnector
    from .json_converter import JSONConverter
    from .constants import Constants
    from .api_response import APIResponse
    from ..header_map import HeaderMap
    from ..header import Header
    from ..parameter_map import ParameterMap
    from ..param import Param
    from zcrmsdk.src.com.zoho.api.exception import SDKException


class CommonAPIHandler(object):

    """
    This class to process the API request and its response.
    Construct the objects that are to be sent as parameters or request body with the API.
    The Request parameter, header and body objects are constructed here.
    Process the response JSON and converts it to relevant objects in the library.
    """

    def __init__(self):

        self.api_path = None
        self.header = HeaderMap()
        self.param = ParameterMap()
        self.request = None
        self.http_method = None
        self.module_api_name = None
        self.content_type = None

    def add_param(self, param_name, param_value):

        """
        This method to add an API request parameter.
        :param param_name: A str containing the API request parameter name.
        :param param_value: A object containing the API request parameter value.
        """

        if self.param is None:
            self.param = ParameterMap()

        self.param.add(Param(param_name), param_value)

    def add_header(self, header_name, header_value):

        """
        This method to add an API request header.
        :param header_name: A str containing the API request header name.
        :param header_value: A object containing the API request header value.
        """

        if self.header is None:
            self.header = HeaderMap()

        self.header.add(Header(header_name), header_value)

    def api_call(self, class_name, encode_type):

        """
        This method of constructing API request and response details. To make the Zoho CRM API calls.
        :param class_name: A str containing the method return type.
        :param encode_type: A str containing the expected API response content type.
        :return:  A APIResponse representing the Zoho CRM API response instance or None.
        """
        try:
            from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
        except Exception:
            from ..initializer import Initializer

        connector = APIHTTPConnector()
        self.set_api_url(connector)
        connector.request_method = self.http_method
        connector.content_type = self.content_type

        if self.header is not None and len(self.header.header_map) > 0:
            connector.headers = self.header.header_map

        if self.param is not None and len(self.param.parameter_map) > 0:
            connector.parameters = self.param.parameter_map

        Initializer.get_initializer().token.authenticate(connector)
        convert_instance = None

        if self.content_type is not None and (self.http_method == Constants.REQUEST_METHOD_POST or self.http_method == Constants.REQUEST_METHOD_PUT):
            convert_instance = self.get_converter_class_instance(self.content_type)
            request = convert_instance.form_request(self.request, self.request.__class__.__module__, 1)
            connector.request_body = request

        connector.headers[Constants.ZOHO_SDK] = platform.system() + "/" + platform.release() + " python/" + platform.python_version() + ":" + Constants.SDK_VERSION
        response = connector.fire_request(convert_instance)
        status_code = response.status_code
        headers = response.headers
        content_type = response.headers[Constants.CONTENT_TYPE]

        if ";" in content_type:
            content_type = content_type.rpartition(";")[0]

        convert_instance = self.get_converter_class_instance(content_type)
        class_name = str(class_name)
        return_object = convert_instance.get_wrapped_response(response, class_name)

        return APIResponse(headers, status_code, return_object)

    def set_api_url(self, connector):
        try:
            from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
        except Exception:
            from ..initializer import Initializer

        api_path = ''

        if 'http' in self.api_path:
            if 'content.zohoapis.com' in self.api_path:
                api_path = Initializer.get_initializer().environment.file_upload_url

                try:
                    url_parse = urllib.parse.urlparse(self.api_path)
                    path = url_parse[2]
                except Exception as ex:
                    CommonAPIHandler.logger.info("Exception in URL " + str(ex))
                    raise SDKException(None, None, None, ex)

                api_path = api_path + path
            else:
                if str(self.api_path)[:1].__eq__('/'):
                    self.api_path = self.api_path[1:]

                api_path = api_path + self.api_path
        else:
            api_path = Initializer.get_initializer().environment.url
            api_path = api_path + self.api_path

        connector.url = api_path

    def get_converter_class_instance(self, encode_type):

        """
        This method to get a Converter class instance.
        :param encode_type: A str containing the API response content type.
        :return: A Converter class instance.
        """

        switcher = {

            "application/json": JSONConverter(self),

            "text/plain": JSONConverter(self),

            "application/xml": XMLConverter(self),

            "text/xml": XMLConverter(self),

            "multipart/form-data": FormDataConverter(self),

            "application/x-download": Downloader(self),

            "image/png": Downloader(self),

            "image/jpeg": Downloader(self),

            "application/zip": Downloader(self),

            "image/gif": Downloader(self),

            "text/csv": Downloader(self),

            "image/tiff": Downloader(self),
        }

        return switcher.get(encode_type, None)
