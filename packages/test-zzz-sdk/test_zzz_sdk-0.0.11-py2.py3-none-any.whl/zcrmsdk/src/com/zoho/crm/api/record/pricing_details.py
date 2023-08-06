try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.record.record import Record
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from .record import Record


class PricingDetails(Record):
	def __init__(self):
		"""Creates an instance of PricingDetails"""
		super().__init__()


	def get_to_range(self):
		"""
		The method to get the to_range

		Returns:
			float: A float value
		"""

		return self.get_key_value('to_range')

	def set_to_range(self, to_range):
		"""
		The method to set the value to to_range

		Parameters:
			to_range (float) : A float value
		"""

		if not isinstance(to_range, float):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: to_range EXPECTED TYPE: float', None, None)
		
		self.add_key_value('to_range', to_range)

	def get_discount(self):
		"""
		The method to get the discount

		Returns:
			float: A float value
		"""

		return self.get_key_value('discount')

	def set_discount(self, discount):
		"""
		The method to set the value to discount

		Parameters:
			discount (float) : A float value
		"""

		if not isinstance(discount, float):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: discount EXPECTED TYPE: float', None, None)
		
		self.add_key_value('discount', discount)

	def get_from_range(self):
		"""
		The method to get the from_range

		Returns:
			float: A float value
		"""

		return self.get_key_value('from_range')

	def set_from_range(self, from_range):
		"""
		The method to set the value to from_range

		Parameters:
			from_range (float) : A float value
		"""

		if not isinstance(from_range, float):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: from_range EXPECTED TYPE: float', None, None)
		
		self.add_key_value('from_range', from_range)

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
