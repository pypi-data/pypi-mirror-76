try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class Attachment(object):
	def __init__(self):
		"""Creates an instance of Attachment"""

		self.__owner = None
		self.__modified_time = None
		self.__file_name = None
		self.__created_time = None
		self.__size = None
		self.__parent_id = None
		self.__editable = None
		self.__file_id = None
		self.__type = None
		self.__se_module = None
		self.__modified_by = None
		self.__state = None
		self.__id = None
		self.__created_by = None
		self.__link_url = None
		self.__description = None
		self.__category = None
		self.__key_modified = dict()

	def get_owner(self):
		"""
		The method to get the owner

		Returns:
			User: An instance of User
		"""

		return self.__owner

	def set_owner(self, owner):
		"""
		The method to set the value to owner

		Parameters:
			owner (User) : An instance of User
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.users import User
		except Exception:
			from ..users import User

		if not isinstance(owner, User):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: owner EXPECTED TYPE: User', None, None)
		
		self.__owner = owner
		self.__key_modified['Owner'] = 1

	def get_modified_time(self):
		"""
		The method to get the modified_time

		Returns:
			datetime: An instance of datetime
		"""

		return self.__modified_time

	def set_modified_time(self, modified_time):
		"""
		The method to set the value to modified_time

		Parameters:
			modified_time (datetime) : An instance of datetime
		"""

		from datetime import datetime

		if not isinstance(modified_time, datetime):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: modified_time EXPECTED TYPE: datetime', None, None)
		
		self.__modified_time = modified_time
		self.__key_modified['Modified_Time'] = 1

	def get_file_name(self):
		"""
		The method to get the file_name

		Returns:
			string: A string value
		"""

		return self.__file_name

	def set_file_name(self, file_name):
		"""
		The method to set the value to file_name

		Parameters:
			file_name (string) : A string value
		"""

		if not isinstance(file_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: file_name EXPECTED TYPE: str', None, None)
		
		self.__file_name = file_name
		self.__key_modified['File_Name'] = 1

	def get_created_time(self):
		"""
		The method to get the created_time

		Returns:
			datetime: An instance of datetime
		"""

		return self.__created_time

	def set_created_time(self, created_time):
		"""
		The method to set the value to created_time

		Parameters:
			created_time (datetime) : An instance of datetime
		"""

		from datetime import datetime

		if not isinstance(created_time, datetime):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: created_time EXPECTED TYPE: datetime', None, None)
		
		self.__created_time = created_time
		self.__key_modified['Created_Time'] = 1

	def get_size(self):
		"""
		The method to get the size

		Returns:
			int: A int value
		"""

		return self.__size

	def set_size(self, size):
		"""
		The method to set the value to size

		Parameters:
			size (int) : A int value
		"""

		if not isinstance(size, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: size EXPECTED TYPE: int', None, None)
		
		self.__size = size
		self.__key_modified['Size'] = 1

	def get_parent_id(self):
		"""
		The method to get the parent_id

		Returns:
			Record: An instance of Record
		"""

		return self.__parent_id

	def set_parent_id(self, parent_id):
		"""
		The method to set the value to parent_id

		Parameters:
			parent_id (Record) : An instance of Record
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.record import Record
		except Exception:
			from ..record import Record

		if not isinstance(parent_id, Record):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: parent_id EXPECTED TYPE: Record', None, None)
		
		self.__parent_id = parent_id
		self.__key_modified['Parent_Id'] = 1

	def get_editable(self):
		"""
		The method to get the editable

		Returns:
			bool: A bool value
		"""

		return self.__editable

	def set_editable(self, editable):
		"""
		The method to set the value to editable

		Parameters:
			editable (bool) : A bool value
		"""

		if not isinstance(editable, bool):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: editable EXPECTED TYPE: bool', None, None)
		
		self.__editable = editable
		self.__key_modified['$editable'] = 1

	def get_file_id(self):
		"""
		The method to get the file_id

		Returns:
			string: A string value
		"""

		return self.__file_id

	def set_file_id(self, file_id):
		"""
		The method to set the value to file_id

		Parameters:
			file_id (string) : A string value
		"""

		if not isinstance(file_id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: file_id EXPECTED TYPE: str', None, None)
		
		self.__file_id = file_id
		self.__key_modified['$file_id'] = 1

	def get_type(self):
		"""
		The method to get the type

		Returns:
			string: A string value
		"""

		return self.__type

	def set_type(self, type):
		"""
		The method to set the value to type

		Parameters:
			type (string) : A string value
		"""

		if not isinstance(type, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: type EXPECTED TYPE: str', None, None)
		
		self.__type = type
		self.__key_modified['$type'] = 1

	def get_se_module(self):
		"""
		The method to get the se_module

		Returns:
			string: A string value
		"""

		return self.__se_module

	def set_se_module(self, se_module):
		"""
		The method to set the value to se_module

		Parameters:
			se_module (string) : A string value
		"""

		if not isinstance(se_module, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: se_module EXPECTED TYPE: str', None, None)
		
		self.__se_module = se_module
		self.__key_modified['$se_module'] = 1

	def get_modified_by(self):
		"""
		The method to get the modified_by

		Returns:
			User: An instance of User
		"""

		return self.__modified_by

	def set_modified_by(self, modified_by):
		"""
		The method to set the value to modified_by

		Parameters:
			modified_by (User) : An instance of User
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.users import User
		except Exception:
			from ..users import User

		if not isinstance(modified_by, User):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: modified_by EXPECTED TYPE: User', None, None)
		
		self.__modified_by = modified_by
		self.__key_modified['Modified_By'] = 1

	def get_state(self):
		"""
		The method to get the state

		Returns:
			string: A string value
		"""

		return self.__state

	def set_state(self, state):
		"""
		The method to set the value to state

		Parameters:
			state (string) : A string value
		"""

		if not isinstance(state, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: state EXPECTED TYPE: str', None, None)
		
		self.__state = state
		self.__key_modified['$state'] = 1

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

	def get_created_by(self):
		"""
		The method to get the created_by

		Returns:
			User: An instance of User
		"""

		return self.__created_by

	def set_created_by(self, created_by):
		"""
		The method to set the value to created_by

		Parameters:
			created_by (User) : An instance of User
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.users import User
		except Exception:
			from ..users import User

		if not isinstance(created_by, User):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: created_by EXPECTED TYPE: User', None, None)
		
		self.__created_by = created_by
		self.__key_modified['Created_By'] = 1

	def get_link_url(self):
		"""
		The method to get the link_url

		Returns:
			string: A string value
		"""

		return self.__link_url

	def set_link_url(self, link_url):
		"""
		The method to set the value to link_url

		Parameters:
			link_url (string) : A string value
		"""

		if not isinstance(link_url, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: link_url EXPECTED TYPE: str', None, None)
		
		self.__link_url = link_url
		self.__key_modified['$link_url'] = 1

	def get_description(self):
		"""
		The method to get the description

		Returns:
			string: A string value
		"""

		return self.__description

	def set_description(self, description):
		"""
		The method to set the value to description

		Parameters:
			description (string) : A string value
		"""

		if not isinstance(description, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: description EXPECTED TYPE: str', None, None)
		
		self.__description = description
		self.__key_modified['description'] = 1

	def get_category(self):
		"""
		The method to get the category

		Returns:
			string: A string value
		"""

		return self.__category

	def set_category(self, category):
		"""
		The method to set the value to category

		Parameters:
			category (string) : A string value
		"""

		if not isinstance(category, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: category EXPECTED TYPE: str', None, None)
		
		self.__category = category
		self.__key_modified['category'] = 1

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
