try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class RecurringActivity(object):
	def __init__(self):
		"""Creates an instance of RecurringActivity"""

		self.__rrule = None
		self.__key_modified = dict()

	def get_rrule(self):
		"""
		The method to get the rrule

		Returns:
			string: A string value
		"""

		return self.__rrule

	def set_rrule(self, rrule):
		"""
		The method to set the value to rrule

		Parameters:
			rrule (string) : A string value
		"""

		if not isinstance(rrule, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: rrule EXPECTED TYPE: str', None, None)
		
		self.__rrule = rrule
		self.__key_modified['RRULE'] = 1

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
