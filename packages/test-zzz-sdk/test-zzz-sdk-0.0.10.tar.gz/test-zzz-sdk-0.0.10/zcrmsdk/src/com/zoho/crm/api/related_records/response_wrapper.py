try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.related_records.response_handler import ResponseHandler
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from .response_handler import ResponseHandler


class ResponseWrapper(ResponseHandler):
	def __init__(self):
		"""Creates an instance of ResponseWrapper"""

		self.__data = None
		self.__info = None
		self.__key_modified = dict()

	def get_data(self):
		"""
		The method to get the data

		Returns:
			list: An instance of list
		"""

		return self.__data

	def set_data(self, data):
		"""
		The method to set the value to data

		Parameters:
			data (list) : An instance of list
		"""

		if not isinstance(data, list):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: data EXPECTED TYPE: list', None, None)
		
		self.__data = data
		self.__key_modified['data'] = 1

	def get_info(self):
		"""
		The method to get the info

		Returns:
			Info: An instance of Info
		"""

		return self.__info

	def set_info(self, info):
		"""
		The method to set the value to info

		Parameters:
			info (Info) : An instance of Info
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.record import Info
		except Exception:
			from ..record import Info

		if not isinstance(info, Info):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: info EXPECTED TYPE: Info', None, None)
		
		self.__info = info
		self.__key_modified['info'] = 1

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
