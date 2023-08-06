try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class ViewType(object):
	def __init__(self):
		"""Creates an instance of ViewType"""

		self.__view = None
		self.__edit = None
		self.__create = None
		self.__quick_create = None
		self.__key_modified = dict()

	def get_view(self):
		"""
		The method to get the view

		Returns:
			bool: A bool value
		"""

		return self.__view

	def set_view(self, view):
		"""
		The method to set the value to view

		Parameters:
			view (bool) : A bool value
		"""

		if not isinstance(view, bool):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: view EXPECTED TYPE: bool', None, None)
		
		self.__view = view
		self.__key_modified['view'] = 1

	def get_edit(self):
		"""
		The method to get the edit

		Returns:
			bool: A bool value
		"""

		return self.__edit

	def set_edit(self, edit):
		"""
		The method to set the value to edit

		Parameters:
			edit (bool) : A bool value
		"""

		if not isinstance(edit, bool):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: edit EXPECTED TYPE: bool', None, None)
		
		self.__edit = edit
		self.__key_modified['edit'] = 1

	def get_create(self):
		"""
		The method to get the create

		Returns:
			bool: A bool value
		"""

		return self.__create

	def set_create(self, create):
		"""
		The method to set the value to create

		Parameters:
			create (bool) : A bool value
		"""

		if not isinstance(create, bool):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: create EXPECTED TYPE: bool', None, None)
		
		self.__create = create
		self.__key_modified['create'] = 1

	def get_quick_create(self):
		"""
		The method to get the quick_create

		Returns:
			bool: A bool value
		"""

		return self.__quick_create

	def set_quick_create(self, quick_create):
		"""
		The method to set the value to quick_create

		Parameters:
			quick_create (bool) : A bool value
		"""

		if not isinstance(quick_create, bool):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: quick_create EXPECTED TYPE: bool', None, None)
		
		self.__quick_create = quick_create
		self.__key_modified['quick_create'] = 1

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
