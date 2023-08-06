try:
	from zcrmsdk.src.com.zoho.crm.api.util import APIResponse, CommonAPIHandler, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import APIResponse, CommonAPIHandler, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class BulkReadOperations(object):
	def __init__(self):
		"""Creates an instance of BulkReadOperations"""
		pass

	def get_bulk_read_job_details(self, job_id):
		"""
		The method to get bulk read job details

		Parameters:
			job_id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""

		if not isinstance(job_id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: job_id EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/bulk/v2/read/'
		api_path = api_path + str(job_id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		try:
			from zcrmsdk.src.com.zoho.crm.api.bulk_read.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def download_result(self, job_id):
		"""
		The method to download result

		Parameters:
			job_id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""

		if not isinstance(job_id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: job_id EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/bulk/v2/read/'
		api_path = api_path + str(job_id)
		api_path = api_path + '/result'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		try:
			from zcrmsdk.src.com.zoho.crm.api.bulk_read.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/x-download')

	def create_bulk_read_job(self, request):
		"""
		The method to create bulk read job

		Parameters:
			request (RequestWrapper) : An instance of RequestWrapper

		Returns:
			APIResponse: An instance of APIResponse
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.bulk_read.request_wrapper import RequestWrapper
		except Exception:
			from .request_wrapper import RequestWrapper

		if not isinstance(request, RequestWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: RequestWrapper', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/bulk/v2/read'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		try:
			from zcrmsdk.src.com.zoho.crm.api.bulk_read.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')
