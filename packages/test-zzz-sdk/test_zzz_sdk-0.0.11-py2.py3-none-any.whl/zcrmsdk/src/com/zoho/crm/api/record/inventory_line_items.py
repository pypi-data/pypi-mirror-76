try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.record.record import Record
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from .record import Record


class InventoryLineItems(Record):
	def __init__(self):
		"""Creates an instance of InventoryLineItems"""
		super().__init__()


	def get_product(self):
		"""
		The method to get the product

		Returns:
			LineItemProduct: An instance of LineItemProduct
		"""

		return self.get_key_value('product')

	def set_product(self, product):
		"""
		The method to set the value to product

		Parameters:
			product (LineItemProduct) : An instance of LineItemProduct
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.record.line_item_product import LineItemProduct
		except Exception:
			from .line_item_product import LineItemProduct

		if not isinstance(product, LineItemProduct):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: product EXPECTED TYPE: LineItemProduct', None, None)
		
		self.add_key_value('product', product)

	def get_quantity(self):
		"""
		The method to get the quantity

		Returns:
			float: A float value
		"""

		return self.get_key_value('quantity')

	def set_quantity(self, quantity):
		"""
		The method to set the value to quantity

		Parameters:
			quantity (float) : A float value
		"""

		if not isinstance(quantity, float):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: quantity EXPECTED TYPE: float', None, None)
		
		self.add_key_value('quantity', quantity)

	def get_discount(self):
		"""
		The method to get the discount

		Returns:
			string: A string value
		"""

		return self.get_key_value('Discount')

	def set_discount(self, discount):
		"""
		The method to set the value to discount

		Parameters:
			discount (string) : A string value
		"""

		if not isinstance(discount, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: discount EXPECTED TYPE: str', None, None)
		
		self.add_key_value('Discount', discount)

	def get_total_after_discount(self):
		"""
		The method to get the total_after_discount

		Returns:
			float: A float value
		"""

		return self.get_key_value('total_after_discount')

	def set_total_after_discount(self, total_after_discount):
		"""
		The method to set the value to total_after_discount

		Parameters:
			total_after_discount (float) : A float value
		"""

		if not isinstance(total_after_discount, float):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: total_after_discount EXPECTED TYPE: float', None, None)
		
		self.add_key_value('total_after_discount', total_after_discount)

	def get_net_total(self):
		"""
		The method to get the net_total

		Returns:
			float: A float value
		"""

		return self.get_key_value('net_total')

	def set_net_total(self, net_total):
		"""
		The method to set the value to net_total

		Parameters:
			net_total (float) : A float value
		"""

		if not isinstance(net_total, float):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: net_total EXPECTED TYPE: float', None, None)
		
		self.add_key_value('net_total', net_total)

	def get_book(self):
		"""
		The method to get the book

		Returns:
			float: A float value
		"""

		return self.get_key_value('book')

	def set_book(self, book):
		"""
		The method to set the value to book

		Parameters:
			book (float) : A float value
		"""

		if not isinstance(book, float):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: book EXPECTED TYPE: float', None, None)
		
		self.add_key_value('book', book)

	def get_tax(self):
		"""
		The method to get the tax

		Returns:
			float: A float value
		"""

		return self.get_key_value('Tax')

	def set_tax(self, tax):
		"""
		The method to set the value to tax

		Parameters:
			tax (float) : A float value
		"""

		if not isinstance(tax, float):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: tax EXPECTED TYPE: float', None, None)
		
		self.add_key_value('Tax', tax)

	def get_list_price(self):
		"""
		The method to get the list_price

		Returns:
			float: A float value
		"""

		return self.get_key_value('list_price')

	def set_list_price(self, list_price):
		"""
		The method to set the value to list_price

		Parameters:
			list_price (float) : A float value
		"""

		if not isinstance(list_price, float):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: list_price EXPECTED TYPE: float', None, None)
		
		self.add_key_value('list_price', list_price)

	def get_unit_price(self):
		"""
		The method to get the unit_price

		Returns:
			float: A float value
		"""

		return self.get_key_value('unit_price')

	def set_unit_price(self, unit_price):
		"""
		The method to set the value to unit_price

		Parameters:
			unit_price (float) : A float value
		"""

		if not isinstance(unit_price, float):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: unit_price EXPECTED TYPE: float', None, None)
		
		self.add_key_value('unit_price', unit_price)

	def get_quantity_in_stock(self):
		"""
		The method to get the quantity_in_stock

		Returns:
			float: A float value
		"""

		return self.get_key_value('quantity_in_stock')

	def set_quantity_in_stock(self, quantity_in_stock):
		"""
		The method to set the value to quantity_in_stock

		Parameters:
			quantity_in_stock (float) : A float value
		"""

		if not isinstance(quantity_in_stock, float):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: quantity_in_stock EXPECTED TYPE: float', None, None)
		
		self.add_key_value('quantity_in_stock', quantity_in_stock)

	def get_total(self):
		"""
		The method to get the total

		Returns:
			float: A float value
		"""

		return self.get_key_value('total')

	def set_total(self, total):
		"""
		The method to set the value to total

		Parameters:
			total (float) : A float value
		"""

		if not isinstance(total, float):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: total EXPECTED TYPE: float', None, None)
		
		self.add_key_value('total', total)

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

	def get_product_description(self):
		"""
		The method to get the product_description

		Returns:
			string: A string value
		"""

		return self.get_key_value('product_description')

	def set_product_description(self, product_description):
		"""
		The method to set the value to product_description

		Parameters:
			product_description (string) : A string value
		"""

		if not isinstance(product_description, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: product_description EXPECTED TYPE: str', None, None)
		
		self.add_key_value('product_description', product_description)

	def get_line_tax(self):
		"""
		The method to get the line_tax

		Returns:
			list: An instance of list
		"""

		return self.get_key_value('line_tax')

	def set_line_tax(self, line_tax):
		"""
		The method to set the value to line_tax

		Parameters:
			line_tax (list) : An instance of list
		"""

		if not isinstance(line_tax, list):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: line_tax EXPECTED TYPE: list', None, None)
		
		self.add_key_value('line_tax', line_tax)
