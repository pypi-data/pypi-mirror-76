from ..util import Model


class PermissionDetail(Model):
	def __init__(self):
		self.__display_label = None
		self.__module = None
		self.__name = None
		self.__id = None
		self.__enabled = None
		self.__key_modified = dict()

	def get_display_label(self):
		"""
		The method to get the display_label

		Returns:
			string: A string value
		"""
		return self.__display_label

	def set_display_label(self, display_label):
		"""
		The method to set the value to display_label

		Parameters:
			display_label (string) : A string value
		"""
		self.__display_label = display_label
		self.__key_modified["display_label"] = 1

	def get_module(self):
		"""
		The method to get the module

		Returns:
			string: A string value
		"""
		return self.__module

	def set_module(self, module):
		"""
		The method to set the value to module

		Parameters:
			module (string) : A string value
		"""
		self.__module = module
		self.__key_modified["module"] = 1

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

	def get_id(self):
		"""
		The method to get the id

		Returns:
			string: A string value
		"""
		return self.__id

	def set_id(self, id):
		"""
		The method to set the value to id

		Parameters:
			id (string) : A string value
		"""
		self.__id = id
		self.__key_modified["id"] = 1

	def get_enabled(self):
		"""
		The method to get the enabled

		Returns:
			bool: A bool value
		"""
		return self.__enabled

	def set_enabled(self, enabled):
		"""
		The method to set the value to enabled

		Parameters:
			enabled (bool) : A bool value
		"""
		self.__enabled = enabled
		self.__key_modified["enabled"] = 1

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
