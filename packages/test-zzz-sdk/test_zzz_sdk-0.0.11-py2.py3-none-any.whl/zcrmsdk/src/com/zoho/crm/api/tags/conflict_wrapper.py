try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class ConflictWrapper(object):
	def __init__(self):
		"""Creates an instance of ConflictWrapper"""

		self.__conflict_id = None
		self.__key_modified = dict()

	def get_conflict_id(self):
		"""
		The method to get the conflict_id

		Returns:
			string: A string value
		"""

		return self.__conflict_id

	def set_conflict_id(self, conflict_id):
		"""
		The method to set the value to conflict_id

		Parameters:
			conflict_id (string) : A string value
		"""

		if not isinstance(conflict_id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: conflict_id EXPECTED TYPE: str', None, None)
		
		self.__conflict_id = conflict_id
		self.__key_modified['conflict_id'] = 1

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
