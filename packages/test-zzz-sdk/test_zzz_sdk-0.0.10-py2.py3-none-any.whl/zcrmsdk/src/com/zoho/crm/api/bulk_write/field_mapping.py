try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class FieldMapping(object):
	def __init__(self):
		"""Creates an instance of FieldMapping"""

		self.__api_name = None
		self.__index = None
		self.__format = None
		self.__find_by = None
		self.__default_value = None
		self.__key_modified = dict()

	def get_api_name(self):
		"""
		The method to get the api_name

		Returns:
			string: A string value
		"""

		return self.__api_name

	def set_api_name(self, api_name):
		"""
		The method to set the value to api_name

		Parameters:
			api_name (string) : A string value
		"""

		if not isinstance(api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: api_name EXPECTED TYPE: str', None, None)
		
		self.__api_name = api_name
		self.__key_modified['api_name'] = 1

	def get_index(self):
		"""
		The method to get the index

		Returns:
			int: A int value
		"""

		return self.__index

	def set_index(self, index):
		"""
		The method to set the value to index

		Parameters:
			index (int) : A int value
		"""

		if not isinstance(index, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: index EXPECTED TYPE: int', None, None)
		
		self.__index = index
		self.__key_modified['index'] = 1

	def get_format(self):
		"""
		The method to get the format

		Returns:
			string: A string value
		"""

		return self.__format

	def set_format(self, format):
		"""
		The method to set the value to format

		Parameters:
			format (string) : A string value
		"""

		if not isinstance(format, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: format EXPECTED TYPE: str', None, None)
		
		self.__format = format
		self.__key_modified['format'] = 1

	def get_find_by(self):
		"""
		The method to get the find_by

		Returns:
			string: A string value
		"""

		return self.__find_by

	def set_find_by(self, find_by):
		"""
		The method to set the value to find_by

		Parameters:
			find_by (string) : A string value
		"""

		if not isinstance(find_by, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: find_by EXPECTED TYPE: str', None, None)
		
		self.__find_by = find_by
		self.__key_modified['find_by'] = 1

	def get_default_value(self):
		"""
		The method to get the default_value

		Returns:
			dict: An instance of dict
		"""

		return self.__default_value

	def set_default_value(self, default_value):
		"""
		The method to set the value to default_value

		Parameters:
			default_value (dict) : An instance of dict
		"""

		if not isinstance(default_value, dict):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: default_value EXPECTED TYPE: dict', None, None)
		
		self.__default_value = default_value
		self.__key_modified['default_value'] = 1

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
