from ..users import User
from ..util import Model


class Profile(Model):
	def __init__(self):
		self.__id = None
		self.__created_time = None
		self.__modified_time = None
		self.__name = None
		self.__default = None
		self.__description = None
		self.__category = None
		self.__modified_by = None
		self.__created_by = None
		self.__permissions_details = None
		self.__sections = None
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

	def get_created_time(self):
		"""
		The method to get the created_time

		Returns:
			DateTime: An instance of DateTime
		"""
		return self.__created_time

	def set_created_time(self, created_time):
		"""
		The method to set the value to created_time

		Parameters:
			created_time (DateTime) : An instance of DateTime
		"""
		self.__created_time = created_time
		self.__key_modified["created_time"] = 1

	def get_modified_time(self):
		"""
		The method to get the modified_time

		Returns:
			DateTime: An instance of DateTime
		"""
		return self.__modified_time

	def set_modified_time(self, modified_time):
		"""
		The method to set the value to modified_time

		Parameters:
			modified_time (DateTime) : An instance of DateTime
		"""
		self.__modified_time = modified_time
		self.__key_modified["modified_time"] = 1

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

	def get_default(self):
		"""
		The method to get the default

		Returns:
			bool: A bool value
		"""
		return self.__default

	def set_default(self, default):
		"""
		The method to set the value to default

		Parameters:
			default (bool) : A bool value
		"""
		self.__default = default
		self.__key_modified["default"] = 1

	def get_description(self):
		"""
		The method to get the description

		Returns:
			string: A string value
		"""
		return self.__description

	def set_description(self, description):
		"""
		The method to set the value to description

		Parameters:
			description (string) : A string value
		"""
		self.__description = description
		self.__key_modified["description"] = 1

	def get_category(self):
		"""
		The method to get the category

		Returns:
			string: A string value
		"""
		return self.__category

	def set_category(self, category):
		"""
		The method to set the value to category

		Parameters:
			category (string) : A string value
		"""
		self.__category = category
		self.__key_modified["category"] = 1

	def get_modified_by(self):
		"""
		The method to get the modified_by

		Returns:
			User: An instance of User
		"""
		return self.__modified_by

	def set_modified_by(self, modified_by):
		"""
		The method to set the value to modified_by

		Parameters:
			modified_by (User) : An instance of User
		"""
		self.__modified_by = modified_by
		self.__key_modified["modified_by"] = 1

	def get_created_by(self):
		"""
		The method to get the created_by

		Returns:
			User: An instance of User
		"""
		return self.__created_by

	def set_created_by(self, created_by):
		"""
		The method to set the value to created_by

		Parameters:
			created_by (User) : An instance of User
		"""
		self.__created_by = created_by
		self.__key_modified["created_by"] = 1

	def get_permissions_details(self):
		"""
		The method to get the permissions_details

		Returns:
			list: An instance of list
		"""
		return self.__permissions_details

	def set_permissions_details(self, permissions_details):
		"""
		The method to set the value to permissions_details

		Parameters:
			permissions_details (list) : An instance of list
		"""
		self.__permissions_details = permissions_details
		self.__key_modified["permissions_details"] = 1

	def get_sections(self):
		"""
		The method to get the sections

		Returns:
			list: An instance of list
		"""
		return self.__sections

	def set_sections(self, sections):
		"""
		The method to set the value to sections

		Parameters:
			sections (list) : An instance of list
		"""
		self.__sections = sections
		self.__key_modified["sections"] = 1

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
