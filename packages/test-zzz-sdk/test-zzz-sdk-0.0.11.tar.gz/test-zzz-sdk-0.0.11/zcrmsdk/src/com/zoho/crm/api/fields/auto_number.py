try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class AutoNumber(object):
	def __init__(self):
		"""Creates an instance of AutoNumber"""

		self.__prefix = None
		self.__suffix = None
		self.__start_number = None
		self.__key_modified = dict()

	def get_prefix(self):
		"""
		The method to get the prefix

		Returns:
			string: A string value
		"""

		return self.__prefix

	def set_prefix(self, prefix):
		"""
		The method to set the value to prefix

		Parameters:
			prefix (string) : A string value
		"""

		if not isinstance(prefix, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: prefix EXPECTED TYPE: str', None, None)
		
		self.__prefix = prefix
		self.__key_modified['prefix'] = 1

	def get_suffix(self):
		"""
		The method to get the suffix

		Returns:
			string: A string value
		"""

		return self.__suffix

	def set_suffix(self, suffix):
		"""
		The method to set the value to suffix

		Parameters:
			suffix (string) : A string value
		"""

		if not isinstance(suffix, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: suffix EXPECTED TYPE: str', None, None)
		
		self.__suffix = suffix
		self.__key_modified['suffix'] = 1

	def get_start_number(self):
		"""
		The method to get the start_number

		Returns:
			int: A int value
		"""

		return self.__start_number

	def set_start_number(self, start_number):
		"""
		The method to set the value to start_number

		Parameters:
			start_number (int) : A int value
		"""

		if not isinstance(start_number, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: start_number EXPECTED TYPE: int', None, None)
		
		self.__start_number = start_number
		self.__key_modified['start_number'] = 1

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
