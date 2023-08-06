from ..util import Model

from .response_handler import ResponseHandler

class ResponseWrapper(Model, ResponseHandler):
	def __init__(self):
		self.__roles = None
		self.__key_modified = dict()

	def get_roles(self):
		"""
		The method to get the roles

		Returns:
			list: An instance of list
		"""
		return self.__roles

	def set_roles(self, roles):
		"""
		The method to set the value to roles

		Parameters:
			roles (list) : An instance of list
		"""
		self.__roles = roles
		self.__key_modified["roles"] = 1

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
