try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class ToolTip(object):
	def __init__(self):
		"""Creates an instance of ToolTip"""

		self.__name = None
		self.__value = None
		self.__key_modified = dict()

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

		if not isinstance(name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: name EXPECTED TYPE: str', None, None)
		
		self.__name = name
		self.__key_modified['name'] = 1

	def get_value(self):
		"""
		The method to get the value

		Returns:
			string: A string value
		"""

		return self.__value

	def set_value(self, value):
		"""
		The method to set the value to value

		Parameters:
			value (string) : A string value
		"""

		if not isinstance(value, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: value EXPECTED TYPE: str', None, None)
		
		self.__value = value
		self.__key_modified['value'] = 1

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
