try:
	from zcrmsdk.src.com.zoho.crm.api.util import APIResponse, CommonAPIHandler, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import APIResponse, CommonAPIHandler, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class LayoutsOperations(object):
	def __init__(self, module):
		"""
		Creates an instance of LayoutsOperations with the given parameters

		Parameters:
			module (string) : A string value
		"""

		if not isinstance(module, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module EXPECTED TYPE: str', None, None)
		
		self.__module = module


	def get_layouts(self):
		"""
		The method to get layouts

		Returns:
			APIResponse: An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/layouts'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.add_param('module', self.__module)
		try:
			from zcrmsdk.src.com.zoho.crm.api.layouts.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def get_layout(self, id):
		"""
		The method to get layout

		Parameters:
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""

		if not isinstance(id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/layouts/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.add_param('module', self.__module)
		try:
			from zcrmsdk.src.com.zoho.crm.api.layouts.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')
