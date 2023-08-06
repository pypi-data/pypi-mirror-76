from ..util import Model


class Group(Model):
	def __init__(self):
		self.__group_operator = None
		self.__comparator = None
		self.__field = None
		self.__value = None
		self.__group = None
		self.__key_modified = dict()

	def get_group_operator(self):
		"""
		The method to get the group_operator

		Returns:
			string: A string value
		"""
		return self.__group_operator

	def set_group_operator(self, group_operator):
		"""
		The method to set the value to group_operator

		Parameters:
			group_operator (string) : A string value
		"""
		self.__group_operator = group_operator
		self.__key_modified["group_operator"] = 1

	def get_comparator(self):
		"""
		The method to get the comparator

		Returns:
			string: A string value
		"""
		return self.__comparator

	def set_comparator(self, comparator):
		"""
		The method to set the value to comparator

		Parameters:
			comparator (string) : A string value
		"""
		self.__comparator = comparator
		self.__key_modified["comparator"] = 1

	def get_field(self):
		"""
		The method to get the field

		Returns:
			string: A string value
		"""
		return self.__field

	def set_field(self, field):
		"""
		The method to set the value to field

		Parameters:
			field (string) : A string value
		"""
		self.__field = field
		self.__key_modified["field"] = 1

	def get_value(self):
		"""
		The method to get the value

		Returns:
			string: A string value
		"""
		return self.__value

	def set_value(self, value):
		"""
		The method to set the value to value

		Parameters:
			value (string) : A string value
		"""
		self.__value = value
		self.__key_modified["value"] = 1

	def get_group(self):
		"""
		The method to get the group

		Returns:
			list: An instance of list
		"""
		return self.__group

	def set_group(self, group):
		"""
		The method to set the value to group

		Parameters:
			group (list) : An instance of list
		"""
		self.__group = group
		self.__key_modified["group"] = 1

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
