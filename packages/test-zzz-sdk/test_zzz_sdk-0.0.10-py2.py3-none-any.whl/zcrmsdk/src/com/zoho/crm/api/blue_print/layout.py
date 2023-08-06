from ..util import Model


class Layout(Model):
	def __init__(self):
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
		self.__view = view
		self.__key_modified["view"] = 1

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
		self.__edit = edit
		self.__key_modified["edit"] = 1

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
		self.__create = create
		self.__key_modified["create"] = 1

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
		self.__quick_create = quick_create
		self.__key_modified["quick_create"] = 1

	def is_key_modified(self, key):
		"""
		The method to check if the user has modified the given key

		Parameters:
			key (string) : A string value

		Returns:
			int: A int value
		"""
		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		"""
		The method to mark the given key as modified

		Parameters:
			modification (int) : A int value
			key (string) : A string value
		"""
		self.__key_modified[key] = modification
