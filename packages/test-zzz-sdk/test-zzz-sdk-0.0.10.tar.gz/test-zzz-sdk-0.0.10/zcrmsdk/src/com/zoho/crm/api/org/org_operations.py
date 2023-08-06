try:
	from zcrmsdk.src.com.zoho.crm.api.util import APIResponse, CommonAPIHandler, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import APIResponse, CommonAPIHandler, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class OrgOperations(object):
	def __init__(self):
		"""Creates an instance of OrgOperations"""
		pass

	def get_organization(self):
		"""
		The method to get organization

		Returns:
			APIResponse: An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/org'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		try:
			from zcrmsdk.src.com.zoho.crm.api.org.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def upload_organization_photo(self, request):
		"""
		The method to upload organization photo

		Parameters:
			request (FileBodyWrapper) : An instance of FileBodyWrapper

		Returns:
			APIResponse: An instance of APIResponse
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.org.file_body_wrapper import FileBodyWrapper
		except Exception:
			from .file_body_wrapper import FileBodyWrapper

		if not isinstance(request, FileBodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: FileBodyWrapper', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/org/photo'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.content_type = 'multipart/form-data'
		handler_instance.request = request
		try:
			from zcrmsdk.src.com.zoho.crm.api.org.action_response import ActionResponse
		except Exception:
			from .action_response import ActionResponse
		return handler_instance.api_call(ActionResponse.__module__, 'application/json')
