try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class PermissionDetail(object):
	def __init__(self):
		"""Creates an instance of PermissionDetail"""

		self.__display_label = None
		self.__module = None
		self.__name = None
		self.__id = None
		self.__enabled = None
		self.__key_modified = dict()

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

		if not isinstance(display_label, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: display_label EXPECTED TYPE: str', None, None)
		
		self.__display_label = display_label
		self.__key_modified['display_label'] = 1

	def get_module(self):
		"""
		The method to get the module

		Returns:
			string: A string value
		"""

		return self.__module

	def set_module(self, module):
		"""
		The method to set the value to module

		Parameters:
			module (string) : A string value
		"""

		if not isinstance(module, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module EXPECTED TYPE: str', None, None)
		
		self.__module = module
		self.__key_modified['module'] = 1

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

	def get_enabled(self):
		"""
		The method to get the enabled

		Returns:
			bool: A bool value
		"""

		return self.__enabled

	def set_enabled(self, enabled):
		"""
		The method to set the value to enabled

		Parameters:
			enabled (bool) : A bool value
		"""

		if not isinstance(enabled, bool):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: enabled EXPECTED TYPE: bool', None, None)
		
		self.__enabled = enabled
		self.__key_modified['enabled'] = 1

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
