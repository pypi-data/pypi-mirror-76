try:
	from zcrmsdk.src.com.zoho.crm.api.util import StreamWrapper, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import StreamWrapper, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class FileBodyWrapper(object):
	def __init__(self):
		"""Creates an instance of FileBodyWrapper"""

		self.__file = None
		self.__key_modified = dict()

	def get_file(self):
		"""
		The method to get the file

		Returns:
			StreamWrapper: An instance of StreamWrapper
		"""

		return self.__file

	def set_file(self, file):
		"""
		The method to set the value to file

		Parameters:
			file (StreamWrapper) : An instance of StreamWrapper
		"""

		if not isinstance(file, StreamWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: file EXPECTED TYPE: StreamWrapper', None, None)
		
		self.__file = file
		self.__key_modified['file'] = 1

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
