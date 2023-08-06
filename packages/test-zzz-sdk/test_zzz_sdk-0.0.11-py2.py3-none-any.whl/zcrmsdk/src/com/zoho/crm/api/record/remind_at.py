try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class RemindAt(object):
	def __init__(self):
		"""Creates an instance of RemindAt"""

		self.__alarm = None
		self.__key_modified = dict()

	def get_alarm(self):
		"""
		The method to get the alarm

		Returns:
			string: A string value
		"""

		return self.__alarm

	def set_alarm(self, alarm):
		"""
		The method to set the value to alarm

		Parameters:
			alarm (string) : A string value
		"""

		if not isinstance(alarm, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: alarm EXPECTED TYPE: str', None, None)
		
		self.__alarm = alarm
		self.__key_modified['ALARM'] = 1

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
