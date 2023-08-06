from ..util import APIResponse
from ..util import CommonAPIHandler

class OrganizationOperations(object):
	def __init__(self):
		pass


	def get_organization(self):
		"""
		The method to get organization

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/org"
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, "application/json")
