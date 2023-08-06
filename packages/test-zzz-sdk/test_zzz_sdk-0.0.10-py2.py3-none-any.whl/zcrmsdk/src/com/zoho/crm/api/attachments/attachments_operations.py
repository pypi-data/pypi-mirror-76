try:
	from zcrmsdk.src.com.zoho.crm.api.parameter_map import ParameterMap
	from zcrmsdk.src.com.zoho.crm.api.util import APIResponse, CommonAPIHandler, Constants
	from zcrmsdk.src.com.zoho.crm.api.param import Param
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..parameter_map import ParameterMap
	from ..util import APIResponse, CommonAPIHandler, Constants
	from ..param import Param
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class AttachmentsOperations(object):
	def __init__(self, record_id, module_api_name):
		"""
		Creates an instance of AttachmentsOperations with the given parameters

		Parameters:
			record_id (string) : A string value
			module_api_name (string) : A string value
		"""

		if not isinstance(record_id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: record_id EXPECTED TYPE: str', None, None)

		if not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)

		self.__record_id = record_id
		self.__module_api_name = module_api_name


	def download_attachment(self, id):
		"""
		The method to download attachment

		Parameters:
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""

		if not isinstance(id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: str', None, None)

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(self.__module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(self.__record_id)
		api_path = api_path + '/Attachments/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		try:
			from zcrmsdk.src.com.zoho.crm.api.attachments.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/x-download')

	def delete_attachment(self, id):
		"""
		The method to delete attachment

		Parameters:
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""

		if not isinstance(id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: str', None, None)

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(self.__module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(self.__record_id)
		api_path = api_path + '/Attachments/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_DELETE
		try:
			from zcrmsdk.src.com.zoho.crm.api.attachments.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def get_attachments(self):
		"""
		The method to get attachments

		Returns:
			APIResponse: An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(self.__module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(self.__record_id)
		api_path = api_path + '/Attachments'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		try:
			from zcrmsdk.src.com.zoho.crm.api.attachments.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def upload_attachment(self, request):
		"""
		The method to upload attachment

		Parameters:
			request (FileBodyWrapper) : An instance of FileBodyWrapper

		Returns:
			APIResponse: An instance of APIResponse
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.attachments.file_body_wrapper import FileBodyWrapper
		except Exception:
			from .file_body_wrapper import FileBodyWrapper

		if not isinstance(request, FileBodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: FileBodyWrapper', None, None)

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(self.__module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(self.__record_id)
		api_path = api_path + '/Attachments'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.content_type = 'multipart/form-data'
		handler_instance.request = request
		try:
			from zcrmsdk.src.com.zoho.crm.api.attachments.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def upload_link_attachment(self, param_instance):
		"""
		The method to upload link attachment

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
			APIResponse: An instance of APIResponse
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(self.__module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(self.__record_id)
		api_path = api_path + '/Attachments'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.param = param_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.attachments.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def delete_attachments(self, param_instance):
		"""
		The method to delete attachments

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
			APIResponse: An instance of APIResponse
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(self.__module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(self.__record_id)
		api_path = api_path + '/Attachments'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_DELETE
		handler_instance.param = param_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.attachments.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')


class UploadLinkAttachmentParam(object):
	attachmenturl = Param('attachmentUrl', 'com.zoho.crm.api.Attachments.UploadLinkAttachmentParam')


class DeleteAttachmentsParam(object):
	ids = Param('ids', 'com.zoho.crm.api.Attachments.DeleteAttachmentsParam')

