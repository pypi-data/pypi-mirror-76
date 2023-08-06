try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class LineItemProduct(object):
	def __init__(self):
		"""Creates an instance of LineItemProduct"""

		self.__product_code = None
		self.__currency = None
		self.__name = None
		self.__id = None
		self.__key_modified = dict()

	def get_product_code(self):
		"""
		The method to get the product_code

		Returns:
			string: A string value
		"""

		return self.__product_code

	def set_product_code(self, product_code):
		"""
		The method to set the value to product_code

		Parameters:
			product_code (string) : A string value
		"""

		if not isinstance(product_code, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: product_code EXPECTED TYPE: str', None, None)
		
		self.__product_code = product_code
		self.__key_modified['Product_Code'] = 1

	def get_currency(self):
		"""
		The method to get the currency

		Returns:
			string: A string value
		"""

		return self.__currency

	def set_currency(self, currency):
		"""
		The method to set the value to currency

		Parameters:
			currency (string) : A string value
		"""

		if not isinstance(currency, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: currency EXPECTED TYPE: str', None, None)
		
		self.__currency = currency
		self.__key_modified['Currency'] = 1

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
