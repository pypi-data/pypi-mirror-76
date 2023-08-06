try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class BodyWrapper(object):
	def __init__(self):
		"""Creates an instance of BodyWrapper"""

		self.__taxes = None
		self.__key_modified = dict()

	def get_taxes(self):
		"""
		The method to get the taxes

		Returns:
			list: An instance of list
		"""

		return self.__taxes

	def set_taxes(self, taxes):
		"""
		The method to set the value to taxes

		Parameters:
			taxes (list) : An instance of list
		"""

		if not isinstance(taxes, list):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: taxes EXPECTED TYPE: list', None, None)
		
		self.__taxes = taxes
		self.__key_modified['taxes'] = 1

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
