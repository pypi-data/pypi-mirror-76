try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class AssociationDetails(object):
	def __init__(self):
		"""Creates an instance of AssociationDetails"""

		self.__lookup_field = None
		self.__related_field = None
		self.__key_modified = dict()

	def get_lookup_field(self):
		"""
		The method to get the lookup_field

		Returns:
			LookupField: An instance of LookupField
		"""

		return self.__lookup_field

	def set_lookup_field(self, lookup_field):
		"""
		The method to set the value to lookup_field

		Parameters:
			lookup_field (LookupField) : An instance of LookupField
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.fields.lookup_field import LookupField
		except Exception:
			from .lookup_field import LookupField

		if not isinstance(lookup_field, LookupField):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: lookup_field EXPECTED TYPE: LookupField', None, None)
		
		self.__lookup_field = lookup_field
		self.__key_modified['lookup_field'] = 1

	def get_related_field(self):
		"""
		The method to get the related_field

		Returns:
			LookupField: An instance of LookupField
		"""

		return self.__related_field

	def set_related_field(self, related_field):
		"""
		The method to set the value to related_field

		Parameters:
			related_field (LookupField) : An instance of LookupField
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.fields.lookup_field import LookupField
		except Exception:
			from .lookup_field import LookupField

		if not isinstance(related_field, LookupField):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: related_field EXPECTED TYPE: LookupField', None, None)
		
		self.__related_field = related_field
		self.__key_modified['related_field'] = 1

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
