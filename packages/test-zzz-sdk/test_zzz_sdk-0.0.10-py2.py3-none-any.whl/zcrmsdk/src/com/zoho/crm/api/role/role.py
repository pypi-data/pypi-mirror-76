from ..users import User
from ..util import Model


class Role(Model):
	def __init__(self):
		self.__id = None
		self.__name = None
		self.__description = None
		self.__display_label = None
		self.__admin_user = None
		self.__share_with_users = None
		self.__reporting_to = None
		self.__forecast_manager = None
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

	def get_admin_user(self):
		"""
		The method to get the admin_user

		Returns:
			bool: A bool value
		"""
		return self.__admin_user

	def set_admin_user(self, admin_user):
		"""
		The method to set the value to admin_user

		Parameters:
			admin_user (bool) : A bool value
		"""
		self.__admin_user = admin_user
		self.__key_modified["admin_user"] = 1

	def get_share_with_users(self):
		"""
		The method to get the share_with_users

		Returns:
			bool: A bool value
		"""
		return self.__share_with_users

	def set_share_with_users(self, share_with_users):
		"""
		The method to set the value to share_with_users

		Parameters:
			share_with_users (bool) : A bool value
		"""
		self.__share_with_users = share_with_users
		self.__key_modified["share_with_users"] = 1

	def get_reporting_to(self):
		"""
		The method to get the reporting_to

		Returns:
			User: An instance of User
		"""
		return self.__reporting_to

	def set_reporting_to(self, reporting_to):
		"""
		The method to set the value to reporting_to

		Parameters:
			reporting_to (User) : An instance of User
		"""
		self.__reporting_to = reporting_to
		self.__key_modified["reporting_to"] = 1

	def get_forecast_manager(self):
		"""
		The method to get the forecast_manager

		Returns:
			User: An instance of User
		"""
		return self.__forecast_manager

	def set_forecast_manager(self, forecast_manager):
		"""
		The method to set the value to forecast_manager

		Parameters:
			forecast_manager (User) : An instance of User
		"""
		self.__forecast_manager = forecast_manager
		self.__key_modified["forecast_manager"] = 1

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
