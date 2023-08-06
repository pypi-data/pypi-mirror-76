from ..util import Model


class RelatedList(Model):
	def __init__(self):
		self.__id = None
		self.__sequence_number = None
		self.__display_label = None
		self.__api_name = None
		self.__module = None
		self.__name = None
		self.__action = None
		self.__href = None
		self.__type = None
		self.__key_modified = dict()

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

	def get_sequence_number(self):
		"""
		The method to get the sequence_number

		Returns:
			string: A string value
		"""
		return self.__sequence_number

	def set_sequence_number(self, sequence_number):
		"""
		The method to set the value to sequence_number

		Parameters:
			sequence_number (string) : A string value
		"""
		self.__sequence_number = sequence_number
		self.__key_modified["sequence_number"] = 1

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

	def get_api_name(self):
		"""
		The method to get the api_name

		Returns:
			string: A string value
		"""
		return self.__api_name

	def set_api_name(self, api_name):
		"""
		The method to set the value to api_name

		Parameters:
			api_name (string) : A string value
		"""
		self.__api_name = api_name
		self.__key_modified["api_name"] = 1

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

	def get_action(self):
		"""
		The method to get the action

		Returns:
			string: A string value
		"""
		return self.__action

	def set_action(self, action):
		"""
		The method to set the value to action

		Parameters:
			action (string) : A string value
		"""
		self.__action = action
		self.__key_modified["action"] = 1

	def get_href(self):
		"""
		The method to get the href

		Returns:
			string: A string value
		"""
		return self.__href

	def set_href(self, href):
		"""
		The method to set the value to href

		Parameters:
			href (string) : A string value
		"""
		self.__href = href
		self.__key_modified["href"] = 1

	def get_type(self):
		"""
		The method to get the type

		Returns:
			string: A string value
		"""
		return self.__type

	def set_type(self, type):
		"""
		The method to set the value to type

		Parameters:
			type (string) : A string value
		"""
		self.__type = type
		self.__key_modified["type"] = 1

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
