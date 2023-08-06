try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class SharedDetails(object):
	def __init__(self):
		"""Creates an instance of SharedDetails"""

		self.__id = None
		self.__name = None
		self.__type = None
		self.__subordinates = None
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

		if not isinstance(id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: str', None, None)
		
		self.__id = id
		self.__key_modified['id'] = 1

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

	def get_type(self):
		"""
		The method to get the type

		Returns:
			string: A string value
		"""

		return self.__type

	def set_type(self, type):
		"""
		The method to set the value to type

		Parameters:
			type (string) : A string value
		"""

		if not isinstance(type, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: type EXPECTED TYPE: str', None, None)
		
		self.__type = type
		self.__key_modified['type'] = 1

	def get_subordinates(self):
		"""
		The method to get the subordinates

		Returns:
			bool: A bool value
		"""

		return self.__subordinates

	def set_subordinates(self, subordinates):
		"""
		The method to set the value to subordinates

		Parameters:
			subordinates (bool) : A bool value
		"""

		if not isinstance(subordinates, bool):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: subordinates EXPECTED TYPE: bool', None, None)
		
		self.__subordinates = subordinates
		self.__key_modified['subordinates'] = 1

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
