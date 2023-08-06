from ..util import Model

from .response_handler import ResponseHandler

class ResponseWrapper(Model, ResponseHandler):
	def __init__(self):
		self.__org = None
		self.__key_modified = dict()

	def get_org(self):
		"""
		The method to get the org

		Returns:
			list: An instance of list
		"""
		return self.__org

	def set_org(self, org):
		"""
		The method to set the value to org

		Parameters:
			org (list) : An instance of list
		"""
		self.__org = org
		self.__key_modified["org"] = 1

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
