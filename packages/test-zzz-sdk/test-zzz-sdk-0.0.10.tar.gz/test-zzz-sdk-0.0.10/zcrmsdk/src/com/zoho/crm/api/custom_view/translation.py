from ..util import Model


class Translation(Model):
	def __init__(self):
		self.__public_views = None
		self.__other_users_views = None
		self.__shared_with_me = None
		self.__created_by_me = None
		self.__key_modified = dict()

	def get_public_views(self):
		"""
		The method to get the public_views

		Returns:
			string: A string value
		"""
		return self.__public_views

	def set_public_views(self, public_views):
		"""
		The method to set the value to public_views

		Parameters:
			public_views (string) : A string value
		"""
		self.__public_views = public_views
		self.__key_modified["public_views"] = 1

	def get_other_users_views(self):
		"""
		The method to get the other_users_views

		Returns:
			string: A string value
		"""
		return self.__other_users_views

	def set_other_users_views(self, other_users_views):
		"""
		The method to set the value to other_users_views

		Parameters:
			other_users_views (string) : A string value
		"""
		self.__other_users_views = other_users_views
		self.__key_modified["other_users_views"] = 1

	def get_shared_with_me(self):
		"""
		The method to get the shared_with_me

		Returns:
			string: A string value
		"""
		return self.__shared_with_me

	def set_shared_with_me(self, shared_with_me):
		"""
		The method to set the value to shared_with_me

		Parameters:
			shared_with_me (string) : A string value
		"""
		self.__shared_with_me = shared_with_me
		self.__key_modified["shared_with_me"] = 1

	def get_created_by_me(self):
		"""
		The method to get the created_by_me

		Returns:
			string: A string value
		"""
		return self.__created_by_me

	def set_created_by_me(self, created_by_me):
		"""
		The method to set the value to created_by_me

		Parameters:
			created_by_me (string) : A string value
		"""
		self.__created_by_me = created_by_me
		self.__key_modified["created_by_me"] = 1

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
