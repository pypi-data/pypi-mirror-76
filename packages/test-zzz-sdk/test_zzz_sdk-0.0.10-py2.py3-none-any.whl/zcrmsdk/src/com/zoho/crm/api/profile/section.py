from ..util import Model


class Section(Model):
	def __init__(self):
		self.__name = None
		self.__categories = None
		self.__key_modified = dict()

	def get_name(self):
		"""
		The method to get the name

		Returns:
			string: A string value
		"""
		return self.__name

	def set_name(self, name):
		"""
		The method to set the value to name

		Parameters:
			name (string) : A string value
		"""
		self.__name = name
		self.__key_modified["name"] = 1

	def get_categories(self):
		"""
		The method to get the categories

		Returns:
			list: An instance of list
		"""
		return self.__categories

	def set_categories(self, categories):
		"""
		The method to set the value to categories

		Parameters:
			categories (list) : An instance of list
		"""
		self.__categories = categories
		self.__key_modified["categories"] = 1

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
