try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class FileDetails(object):
	def __init__(self):
		"""Creates an instance of FileDetails"""

		self.__extn = None
		self.__is_preview_available = None
		self.__download_url = None
		self.__delete_url = None
		self.__entity_id = None
		self.__mode = None
		self.__original_size_byte = None
		self.__preview_url = None
		self.__file_name = None
		self.__file_id = None
		self.__attachment_id = None
		self.__file_size = None
		self.__creator_id = None
		self.__link_docs = None
		self.__delete = None
		self.__key_modified = dict()

	def get_extn(self):
		"""
		The method to get the extn

		Returns:
			string: A string value
		"""

		return self.__extn

	def set_extn(self, extn):
		"""
		The method to set the value to extn

		Parameters:
			extn (string) : A string value
		"""

		if not isinstance(extn, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: extn EXPECTED TYPE: str', None, None)
		
		self.__extn = extn
		self.__key_modified['extn'] = 1

	def get_is_preview_available(self):
		"""
		The method to get the is_preview_available

		Returns:
			bool: A bool value
		"""

		return self.__is_preview_available

	def set_is_preview_available(self, is_preview_available):
		"""
		The method to set the value to is_preview_available

		Parameters:
			is_preview_available (bool) : A bool value
		"""

		if not isinstance(is_preview_available, bool):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: is_preview_available EXPECTED TYPE: bool', None, None)
		
		self.__is_preview_available = is_preview_available
		self.__key_modified['is_Preview_Available'] = 1

	def get_download_url(self):
		"""
		The method to get the download_url

		Returns:
			string: A string value
		"""

		return self.__download_url

	def set_download_url(self, download_url):
		"""
		The method to set the value to download_url

		Parameters:
			download_url (string) : A string value
		"""

		if not isinstance(download_url, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: download_url EXPECTED TYPE: str', None, None)
		
		self.__download_url = download_url
		self.__key_modified['download_Url'] = 1

	def get_delete_url(self):
		"""
		The method to get the delete_url

		Returns:
			string: A string value
		"""

		return self.__delete_url

	def set_delete_url(self, delete_url):
		"""
		The method to set the value to delete_url

		Parameters:
			delete_url (string) : A string value
		"""

		if not isinstance(delete_url, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: delete_url EXPECTED TYPE: str', None, None)
		
		self.__delete_url = delete_url
		self.__key_modified['delete_Url'] = 1

	def get_entity_id(self):
		"""
		The method to get the entity_id

		Returns:
			string: A string value
		"""

		return self.__entity_id

	def set_entity_id(self, entity_id):
		"""
		The method to set the value to entity_id

		Parameters:
			entity_id (string) : A string value
		"""

		if not isinstance(entity_id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: entity_id EXPECTED TYPE: str', None, None)
		
		self.__entity_id = entity_id
		self.__key_modified['entity_Id'] = 1

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

	def get_original_size_byte(self):
		"""
		The method to get the original_size_byte

		Returns:
			string: A string value
		"""

		return self.__original_size_byte

	def set_original_size_byte(self, original_size_byte):
		"""
		The method to set the value to original_size_byte

		Parameters:
			original_size_byte (string) : A string value
		"""

		if not isinstance(original_size_byte, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: original_size_byte EXPECTED TYPE: str', None, None)
		
		self.__original_size_byte = original_size_byte
		self.__key_modified['original_Size_Byte'] = 1

	def get_preview_url(self):
		"""
		The method to get the preview_url

		Returns:
			string: A string value
		"""

		return self.__preview_url

	def set_preview_url(self, preview_url):
		"""
		The method to set the value to preview_url

		Parameters:
			preview_url (string) : A string value
		"""

		if not isinstance(preview_url, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: preview_url EXPECTED TYPE: str', None, None)
		
		self.__preview_url = preview_url
		self.__key_modified['preview_Url'] = 1

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
		self.__key_modified['file_Name'] = 1

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
		self.__key_modified['file_Id'] = 1

	def get_attachment_id(self):
		"""
		The method to get the attachment_id

		Returns:
			string: A string value
		"""

		return self.__attachment_id

	def set_attachment_id(self, attachment_id):
		"""
		The method to set the value to attachment_id

		Parameters:
			attachment_id (string) : A string value
		"""

		if not isinstance(attachment_id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: attachment_id EXPECTED TYPE: str', None, None)
		
		self.__attachment_id = attachment_id
		self.__key_modified['attachment_Id'] = 1

	def get_file_size(self):
		"""
		The method to get the file_size

		Returns:
			string: A string value
		"""

		return self.__file_size

	def set_file_size(self, file_size):
		"""
		The method to set the value to file_size

		Parameters:
			file_size (string) : A string value
		"""

		if not isinstance(file_size, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: file_size EXPECTED TYPE: str', None, None)
		
		self.__file_size = file_size
		self.__key_modified['file_Size'] = 1

	def get_creator_id(self):
		"""
		The method to get the creator_id

		Returns:
			string: A string value
		"""

		return self.__creator_id

	def set_creator_id(self, creator_id):
		"""
		The method to set the value to creator_id

		Parameters:
			creator_id (string) : A string value
		"""

		if not isinstance(creator_id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: creator_id EXPECTED TYPE: str', None, None)
		
		self.__creator_id = creator_id
		self.__key_modified['creator_Id'] = 1

	def get_link_docs(self):
		"""
		The method to get the link_docs

		Returns:
			int: A int value
		"""

		return self.__link_docs

	def set_link_docs(self, link_docs):
		"""
		The method to set the value to link_docs

		Parameters:
			link_docs (int) : A int value
		"""

		if not isinstance(link_docs, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: link_docs EXPECTED TYPE: int', None, None)
		
		self.__link_docs = link_docs
		self.__key_modified['link_Docs'] = 1

	def get_delete(self):
		"""
		The method to get the delete

		Returns:
			string: A string value
		"""

		return self.__delete

	def set_delete(self, delete):
		"""
		The method to set the value to delete

		Parameters:
			delete (string) : A string value
		"""

		if not isinstance(delete, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: delete EXPECTED TYPE: str', None, None)
		
		self.__delete = delete
		self.__key_modified['_delete'] = 1

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
