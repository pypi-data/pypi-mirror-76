try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.record.record import Record
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from .record import Record


class Participants(Record):
	def __init__(self):
		"""Creates an instance of Participants"""
		super().__init__()


	def get_name(self):
		"""
		The method to get the name

		Returns:
			string: A string value
		"""

		return self.get_key_value('name')

	def set_name(self, name):
		"""
		The method to set the value to name

		Parameters:
			name (string) : A string value
		"""

		if not isinstance(name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: name EXPECTED TYPE: str', None, None)
		
		self.add_key_value('name', name)

	def get_invited(self):
		"""
		The method to get the invited

		Returns:
			bool: A bool value
		"""

		return self.get_key_value('invited')

	def set_invited(self, invited):
		"""
		The method to set the value to invited

		Parameters:
			invited (bool) : A bool value
		"""

		if not isinstance(invited, bool):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: invited EXPECTED TYPE: bool', None, None)
		
		self.add_key_value('invited', invited)

	def get_id(self):
		"""
		The method to get the id

		Returns:
			string: A string value
		"""

		return self.get_key_value('id')

	def set_id(self, id):
		"""
		The method to set the value to id

		Parameters:
			id (string) : A string value
		"""

		if not isinstance(id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: str', None, None)
		
		self.add_key_value('id', id)

	def get_type(self):
		"""
		The method to get the type

		Returns:
			string: A string value
		"""

		return self.get_key_value('type')

	def set_type(self, type):
		"""
		The method to set the value to type

		Parameters:
			type (string) : A string value
		"""

		if not isinstance(type, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: type EXPECTED TYPE: str', None, None)
		
		self.add_key_value('type', type)

	def get_participant(self):
		"""
		The method to get the participant

		Returns:
			string: A string value
		"""

		return self.get_key_value('participant')

	def set_participant(self, participant):
		"""
		The method to set the value to participant

		Parameters:
			participant (string) : A string value
		"""

		if not isinstance(participant, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: participant EXPECTED TYPE: str', None, None)
		
		self.add_key_value('participant', participant)

	def get_status(self):
		"""
		The method to get the status

		Returns:
			string: A string value
		"""

		return self.get_key_value('status')

	def set_status(self, status):
		"""
		The method to set the value to status

		Parameters:
			status (string) : A string value
		"""

		if not isinstance(status, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: status EXPECTED TYPE: str', None, None)
		
		self.add_key_value('status', status)
