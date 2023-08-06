try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class Crypt(object):
	def __init__(self):
		"""Creates an instance of Crypt"""

		self.__mode = None
		self.__column = None
		self.__table = None
		self.__status = None
		self.__key_modified = dict()

	def get_mode(self):
		"""
		The method to get the mode

		Returns:
			string: A string value
		"""

		return self.__mode

	def set_mode(self, mode):
		"""
		The method to set the value to mode

		Parameters:
			mode (string) : A string value
		"""

		if not isinstance(mode, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: mode EXPECTED TYPE: str', None, None)
		
		self.__mode = mode
		self.__key_modified['mode'] = 1

	def get_column(self):
		"""
		The method to get the column

		Returns:
			string: A string value
		"""

		return self.__column

	def set_column(self, column):
		"""
		The method to set the value to column

		Parameters:
			column (string) : A string value
		"""

		if not isinstance(column, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: column EXPECTED TYPE: str', None, None)
		
		self.__column = column
		self.__key_modified['column'] = 1

	def get_table(self):
		"""
		The method to get the table

		Returns:
			string: A string value
		"""

		return self.__table

	def set_table(self, table):
		"""
		The method to set the value to table

		Parameters:
			table (string) : A string value
		"""

		if not isinstance(table, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: table EXPECTED TYPE: str', None, None)
		
		self.__table = table
		self.__key_modified['table'] = 1

	def get_status(self):
		"""
		The method to get the status

		Returns:
			int: A int value
		"""

		return self.__status

	def set_status(self, status):
		"""
		The method to set the value to status

		Parameters:
			status (int) : A int value
		"""

		if not isinstance(status, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: status EXPECTED TYPE: int', None, None)
		
		self.__status = status
		self.__key_modified['status'] = 1

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
