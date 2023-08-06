try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class Reminder(object):
	def __init__(self):
		"""Creates an instance of Reminder"""

		self.__period = None
		self.__unit = None
		self.__key_modified = dict()

	def get_period(self):
		"""
		The method to get the period

		Returns:
			string: A string value
		"""

		return self.__period

	def set_period(self, period):
		"""
		The method to set the value to period

		Parameters:
			period (string) : A string value
		"""

		if not isinstance(period, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: period EXPECTED TYPE: str', None, None)
		
		self.__period = period
		self.__key_modified['period'] = 1

	def get_unit(self):
		"""
		The method to get the unit

		Returns:
			string: A string value
		"""

		return self.__unit

	def set_unit(self, unit):
		"""
		The method to set the value to unit

		Parameters:
			unit (string) : A string value
		"""

		if not isinstance(unit, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: unit EXPECTED TYPE: str', None, None)
		
		self.__unit = unit
		self.__key_modified['unit'] = 1

	def is_key_modified(self, key):
		"""
		The method to check if the user has modified the given key

		Parameters:
			key (string) : A string value

		Returns:
			int: A int value
		"""

		if not isinstance(key, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: key EXPECTED TYPE: str', None, None)
		
		if key in self.__key_modified:
			return self.__key_modified.get(key)
		
		return None

	def set_key_modified(self, key, modification):
		"""
		The method to mark the given key as modified

		Parameters:
			key (string) : A string value
			modification (int) : A int value
		"""

		if not isinstance(key, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: key EXPECTED TYPE: str', None, None)
		
		if not isinstance(modification, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: modification EXPECTED TYPE: int', None, None)
		
		self.__key_modified[key] = modification
