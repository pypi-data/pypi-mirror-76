try:
	from zcrmsdk.src.com.zoho.crm.api.util import Choice, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.attachments.action_response import ActionResponse
	from zcrmsdk.src.com.zoho.crm.api.attachments.response_handler import ResponseHandler
	from zcrmsdk.src.com.zoho.crm.api.attachments.action_handler import ActionHandler
except Exception:
	from ..util import Choice, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from .action_response import ActionResponse
	from .response_handler import ResponseHandler
	from .action_handler import ActionHandler


class APIException(ResponseHandler, ActionResponse, ActionHandler):
	def __init__(self):
		"""Creates an instance of APIException"""

		self.__status = None
		self.__code = None
		self.__message = None
		self.__details = None
		self.__key_modified = dict()

	def get_status(self):
		"""
		The method to get the status

		Returns:
			Choice: An instance of Choice
		"""

		return self.__status

	def set_status(self, status):
		"""
		The method to set the value to status

		Parameters:
			status (Choice) : An instance of Choice
		"""

		if not isinstance(status, Choice):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: status EXPECTED TYPE: Choice', None, None)
		
		self.__status = status
		self.__key_modified['status'] = 1

	def get_code(self):
		"""
		The method to get the code

		Returns:
			Choice: An instance of Choice
		"""

		return self.__code

	def set_code(self, code):
		"""
		The method to set the value to code

		Parameters:
			code (Choice) : An instance of Choice
		"""

		if not isinstance(code, Choice):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: code EXPECTED TYPE: Choice', None, None)
		
		self.__code = code
		self.__key_modified['code'] = 1

	def get_message(self):
		"""
		The method to get the message

		Returns:
			Choice: An instance of Choice
		"""

		return self.__message

	def set_message(self, message):
		"""
		The method to set the value to message

		Parameters:
			message (Choice) : An instance of Choice
		"""

		if not isinstance(message, Choice):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: message EXPECTED TYPE: Choice', None, None)
		
		self.__message = message
		self.__key_modified['message'] = 1

	def get_details(self):
		"""
		The method to get the details

		Returns:
			dict: An instance of dict
		"""

		return self.__details

	def set_details(self, details):
		"""
		The method to set the value to details

		Parameters:
			details (dict) : An instance of dict
		"""

		if not isinstance(details, dict):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: details EXPECTED TYPE: dict', None, None)
		
		self.__details = details
		self.__key_modified['details'] = 1

	def is_key_modified(self, key):
		"""
		The method to check if the user has modified the given key

		Parameters:
			key (string) : A string value

		Returns:
			int: A int value
		"""

		if not isinstance(key, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: key EXPECTED TYPE: str', None, None)
		
		if key in self.__key_modified:
			return self.__key_modified.get(key)
		
		return None

	def set_key_modified(self, key, modification):
		"""
		The method to mark the given key as modified

		Parameters:
			key (string) : A string value
			modification (int) : A int value
		"""

		if not isinstance(key, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: key EXPECTED TYPE: str', None, None)
		
		if not isinstance(modification, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: modification EXPECTED TYPE: int', None, None)
		
		self.__key_modified[key] = modification
