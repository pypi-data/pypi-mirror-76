from ..util import Model

from .response_handler import ResponseHandler

class ResponseWrapper(Model, ResponseHandler):
	def __init__(self):
		self.__related_lists = None
		self.__key_modified = dict()

	def get_related_lists(self):
		"""
		The method to get the related_lists

		Returns:
			list: An instance of list
		"""
		return self.__related_lists

	def set_related_lists(self, related_lists):
		"""
		The method to set the value to related_lists

		Parameters:
			related_lists (list) : An instance of list
		"""
		self.__related_lists = related_lists
		self.__key_modified["related_lists"] = 1

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
