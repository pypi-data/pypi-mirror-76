try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class Currency(object):
	def __init__(self):
		"""Creates an instance of Currency"""

		self.__rounding_option = None
		self.__precision = None
		self.__key_modified = dict()

	def get_rounding_option(self):
		"""
		The method to get the rounding_option

		Returns:
			string: A string value
		"""

		return self.__rounding_option

	def set_rounding_option(self, rounding_option):
		"""
		The method to set the value to rounding_option

		Parameters:
			rounding_option (string) : A string value
		"""

		if not isinstance(rounding_option, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: rounding_option EXPECTED TYPE: str', None, None)
		
		self.__rounding_option = rounding_option
		self.__key_modified['rounding_option'] = 1

	def get_precision(self):
		"""
		The method to get the precision

		Returns:
			int: A int value
		"""

		return self.__precision

	def set_precision(self, precision):
		"""
		The method to set the value to precision

		Parameters:
			precision (int) : A int value
		"""

		if not isinstance(precision, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: precision EXPECTED TYPE: int', None, None)
		
		self.__precision = precision
		self.__key_modified['precision'] = 1

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
