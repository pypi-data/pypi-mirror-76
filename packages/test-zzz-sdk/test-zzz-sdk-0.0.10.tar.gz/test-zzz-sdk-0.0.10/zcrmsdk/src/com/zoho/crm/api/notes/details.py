from ..users import User
from ..util import Model


class Details(Model):
	def __init__(self):
		self.__modified_time = None
		self.__modified_by = None
		self.__created_time = None
		self.__id = None
		self.__created_by = None
		self.__key_modified = dict()

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
		self.__key_modified["Modified_Time"] = 1

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
		self.__key_modified["Modified_By"] = 1

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
		self.__key_modified["Created_Time"] = 1

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
		self.__key_modified["Created_By"] = 1

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
