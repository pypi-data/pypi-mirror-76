try:
	from zcrmsdk.src.com.zoho.crm.api.util import APIResponse, CommonAPIHandler, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import APIResponse, CommonAPIHandler, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class ProfilesOperations(object):
	def __init__(self):
		"""Creates an instance of ProfilesOperations"""
		pass

	def get_profiles(self):
		"""
		The method to get profiles

		Returns:
			APIResponse: An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/profiles'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		try:
			from zcrmsdk.src.com.zoho.crm.api.profiles.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def get_profile(self, id):
		"""
		The method to get profile

		Parameters:
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""

		if not isinstance(id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/profiles/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		try:
			from zcrmsdk.src.com.zoho.crm.api.profiles.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')
