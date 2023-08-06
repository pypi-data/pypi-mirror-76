from ..util import Model


class LicenseDetails(Model):
	def __init__(self):
		self.__paid_expiry = None
		self.__users_license_purchased = None
		self.__trial_type = None
		self.__trial_expiry = None
		self.__paid = None
		self.__paid_type = None
		self.__key_modified = dict()

	def get_paid_expiry(self):
		"""
		The method to get the paid_expiry

		Returns:
			DateTime: An instance of DateTime
		"""
		return self.__paid_expiry

	def set_paid_expiry(self, paid_expiry):
		"""
		The method to set the value to paid_expiry

		Parameters:
			paid_expiry (DateTime) : An instance of DateTime
		"""
		self.__paid_expiry = paid_expiry
		self.__key_modified["paid_expiry"] = 1

	def get_users_license_purchased(self):
		"""
		The method to get the users_license_purchased

		Returns:
			string: A string value
		"""
		return self.__users_license_purchased

	def set_users_license_purchased(self, users_license_purchased):
		"""
		The method to set the value to users_license_purchased

		Parameters:
			users_license_purchased (string) : A string value
		"""
		self.__users_license_purchased = users_license_purchased
		self.__key_modified["users_license_purchased"] = 1

	def get_trial_type(self):
		"""
		The method to get the trial_type

		Returns:
			string: A string value
		"""
		return self.__trial_type

	def set_trial_type(self, trial_type):
		"""
		The method to set the value to trial_type

		Parameters:
			trial_type (string) : A string value
		"""
		self.__trial_type = trial_type
		self.__key_modified["trial_type"] = 1

	def get_trial_expiry(self):
		"""
		The method to get the trial_expiry

		Returns:
			string: A string value
		"""
		return self.__trial_expiry

	def set_trial_expiry(self, trial_expiry):
		"""
		The method to set the value to trial_expiry

		Parameters:
			trial_expiry (string) : A string value
		"""
		self.__trial_expiry = trial_expiry
		self.__key_modified["trial_expiry"] = 1

	def get_paid(self):
		"""
		The method to get the paid

		Returns:
			bool: A bool value
		"""
		return self.__paid

	def set_paid(self, paid):
		"""
		The method to set the value to paid

		Parameters:
			paid (bool) : A bool value
		"""
		self.__paid = paid
		self.__key_modified["paid"] = 1

	def get_paid_type(self):
		"""
		The method to get the paid_type

		Returns:
			string: A string value
		"""
		return self.__paid_type

	def set_paid_type(self, paid_type):
		"""
		The method to set the value to paid_type

		Parameters:
			paid_type (string) : A string value
		"""
		self.__paid_type = paid_type
		self.__key_modified["paid_type"] = 1

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
