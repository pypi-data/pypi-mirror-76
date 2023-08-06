from ..util import Model

from .response_handler import ResponseHandler

class APIException(Model, ResponseHandler):
	def __init__(self):
		self.__code = None
		self.__status = None
		self.__message = None
		self.__details = None
		self.__key_modified = dict()

	def get_code(self):
		"""
		The method to get the code

		Returns:
			string: A string value
		"""
		return self.__code

	def set_code(self, code):
		"""
		The method to set the value to code

		Parameters:
			code (string) : A string value
		"""
		self.__code = code
		self.__key_modified["code"] = 1

	def get_status(self):
		"""
		The method to get the status

		Returns:
			string: A string value
		"""
		return self.__status

	def set_status(self, status):
		"""
		The method to set the value to status

		Parameters:
			status (string) : A string value
		"""
		self.__status = status
		self.__key_modified["status"] = 1

	def get_message(self):
		"""
		The method to get the message

		Returns:
			string: A string value
		"""
		return self.__message

	def set_message(self, message):
		"""
		The method to set the value to message

		Parameters:
			message (string) : A string value
		"""
		self.__message = message
		self.__key_modified["message"] = 1

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
		self.__details = details
		self.__key_modified["details"] = 1

	def is_key_modified(self, key):
		"""
		The method to check if the user has modified the given key

		Parameters:
			key (string) : A string value

		Returns:
			int: A int value
		"""
		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		"""
		The method to mark the given key as modified

		Parameters:
			modification (int) : A int value
			key (string) : A string value
		"""
		self.__key_modified[key] = modification
