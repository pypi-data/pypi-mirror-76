try:
	from zcrmsdk.src.com.zoho.crm.api.util import Choice, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Choice, Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class Format(object):
	def __init__(self):
		"""Creates an instance of Format"""

		self.__decimal_separator = None
		self.__thousand_separator = None
		self.__decimal_places = None
		self.__key_modified = dict()

	def get_decimal_separator(self):
		"""
		The method to get the decimal_separator

		Returns:
			Choice: An instance of Choice
		"""

		return self.__decimal_separator

	def set_decimal_separator(self, decimal_separator):
		"""
		The method to set the value to decimal_separator

		Parameters:
			decimal_separator (Choice) : An instance of Choice
		"""

		if not isinstance(decimal_separator, Choice):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: decimal_separator EXPECTED TYPE: Choice', None, None)
		
		self.__decimal_separator = decimal_separator
		self.__key_modified['decimal_separator'] = 1

	def get_thousand_separator(self):
		"""
		The method to get the thousand_separator

		Returns:
			Choice: An instance of Choice
		"""

		return self.__thousand_separator

	def set_thousand_separator(self, thousand_separator):
		"""
		The method to set the value to thousand_separator

		Parameters:
			thousand_separator (Choice) : An instance of Choice
		"""

		if not isinstance(thousand_separator, Choice):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: thousand_separator EXPECTED TYPE: Choice', None, None)
		
		self.__thousand_separator = thousand_separator
		self.__key_modified['thousand_separator'] = 1

	def get_decimal_places(self):
		"""
		The method to get the decimal_places

		Returns:
			Choice: An instance of Choice
		"""

		return self.__decimal_places

	def set_decimal_places(self, decimal_places):
		"""
		The method to set the value to decimal_places

		Parameters:
			decimal_places (Choice) : An instance of Choice
		"""

		if not isinstance(decimal_places, Choice):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: decimal_places EXPECTED TYPE: Choice', None, None)
		
		self.__decimal_places = decimal_places
		self.__key_modified['decimal_places'] = 1

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
