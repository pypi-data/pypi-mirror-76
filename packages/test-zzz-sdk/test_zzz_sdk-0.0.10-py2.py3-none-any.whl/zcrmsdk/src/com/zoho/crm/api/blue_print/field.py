from ..util import Model


class Field(Model):
	def __init__(self):
		self.__webhook = None
		self.__json_type = None
		self.__display_label = None
		self.__data_type = None
		self.__column_name = None
		self.__personality_name = None
		self.__id = None
		self.__transition_sequence = None
		self.__mandatory = None
		self.__layouts = None
		self.__api_name = None
		self.__content = None
		self.__system_mandatory = None
		self.__crypt = None
		self.__field_label = None
		self.__tooltip = None
		self.__created_source = None
		self.__field_read_only = None
		self.__validation_rule = None
		self.__read_only = None
		self.__association_details = None
		self.__quick_sequence_number = None
		self.__custom_field = None
		self.__visible = None
		self.__length = None
		self.__decimal_place = None
		self.__view_type = None
		self.__pick_list_values = None
		self.__multiselectlookup = None
		self.__auto_number = None
		self.__key_modified = dict()

	def get_webhook(self):
		"""
		The method to get the webhook

		Returns:
			bool: A bool value
		"""
		return self.__webhook

	def set_webhook(self, webhook):
		"""
		The method to set the value to webhook

		Parameters:
			webhook (bool) : A bool value
		"""
		self.__webhook = webhook
		self.__key_modified["webhook"] = 1

	def get_json_type(self):
		"""
		The method to get the json_type

		Returns:
			string: A string value
		"""
		return self.__json_type

	def set_json_type(self, json_type):
		"""
		The method to set the value to json_type

		Parameters:
			json_type (string) : A string value
		"""
		self.__json_type = json_type
		self.__key_modified["json_type"] = 1

	def get_display_label(self):
		"""
		The method to get the display_label

		Returns:
			string: A string value
		"""
		return self.__display_label

	def set_display_label(self, display_label):
		"""
		The method to set the value to display_label

		Parameters:
			display_label (string) : A string value
		"""
		self.__display_label = display_label
		self.__key_modified["display_label"] = 1

	def get_data_type(self):
		"""
		The method to get the data_type

		Returns:
			string: A string value
		"""
		return self.__data_type

	def set_data_type(self, data_type):
		"""
		The method to set the value to data_type

		Parameters:
			data_type (string) : A string value
		"""
		self.__data_type = data_type
		self.__key_modified["data_type"] = 1

	def get_column_name(self):
		"""
		The method to get the column_name

		Returns:
			string: A string value
		"""
		return self.__column_name

	def set_column_name(self, column_name):
		"""
		The method to set the value to column_name

		Parameters:
			column_name (string) : A string value
		"""
		self.__column_name = column_name
		self.__key_modified["column_name"] = 1

	def get_personality_name(self):
		"""
		The method to get the personality_name

		Returns:
			string: A string value
		"""
		return self.__personality_name

	def set_personality_name(self, personality_name):
		"""
		The method to set the value to personality_name

		Parameters:
			personality_name (string) : A string value
		"""
		self.__personality_name = personality_name
		self.__key_modified["personality_name"] = 1

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
		self.__id = id
		self.__key_modified["id"] = 1

	def get_transition_sequence(self):
		"""
		The method to get the transition_sequence

		Returns:
			int: A int value
		"""
		return self.__transition_sequence

	def set_transition_sequence(self, transition_sequence):
		"""
		The method to set the value to transition_sequence

		Parameters:
			transition_sequence (int) : A int value
		"""
		self.__transition_sequence = transition_sequence
		self.__key_modified["transition_sequence"] = 1

	def get_mandatory(self):
		"""
		The method to get the mandatory

		Returns:
			bool: A bool value
		"""
		return self.__mandatory

	def set_mandatory(self, mandatory):
		"""
		The method to set the value to mandatory

		Parameters:
			mandatory (bool) : A bool value
		"""
		self.__mandatory = mandatory
		self.__key_modified["mandatory"] = 1

	def get_layouts(self):
		"""
		The method to get the layouts

		Returns:
			list: An instance of list
		"""
		return self.__layouts

	def set_layouts(self, layouts):
		"""
		The method to set the value to layouts

		Parameters:
			layouts (list) : An instance of list
		"""
		self.__layouts = layouts
		self.__key_modified["layouts"] = 1

	def get_api_name(self):
		"""
		The method to get the api_name

		Returns:
			string: A string value
		"""
		return self.__api_name

	def set_api_name(self, api_name):
		"""
		The method to set the value to api_name

		Parameters:
			api_name (string) : A string value
		"""
		self.__api_name = api_name
		self.__key_modified["api_name"] = 1

	def get_content(self):
		"""
		The method to get the content

		Returns:
			string: A string value
		"""
		return self.__content

	def set_content(self, content):
		"""
		The method to set the value to content

		Parameters:
			content (string) : A string value
		"""
		self.__content = content
		self.__key_modified["content"] = 1

	def get_system_mandatory(self):
		"""
		The method to get the system_mandatory

		Returns:
			bool: A bool value
		"""
		return self.__system_mandatory

	def set_system_mandatory(self, system_mandatory):
		"""
		The method to set the value to system_mandatory

		Parameters:
			system_mandatory (bool) : A bool value
		"""
		self.__system_mandatory = system_mandatory
		self.__key_modified["system_mandatory"] = 1

	def get_crypt(self):
		"""
		The method to get the crypt

		Returns:
			string: A string value
		"""
		return self.__crypt

	def set_crypt(self, crypt):
		"""
		The method to set the value to crypt

		Parameters:
			crypt (string) : A string value
		"""
		self.__crypt = crypt
		self.__key_modified["crypt"] = 1

	def get_field_label(self):
		"""
		The method to get the field_label

		Returns:
			string: A string value
		"""
		return self.__field_label

	def set_field_label(self, field_label):
		"""
		The method to set the value to field_label

		Parameters:
			field_label (string) : A string value
		"""
		self.__field_label = field_label
		self.__key_modified["field_label"] = 1

	def get_tooltip(self):
		"""
		The method to get the tooltip

		Returns:
			string: A string value
		"""
		return self.__tooltip

	def set_tooltip(self, tooltip):
		"""
		The method to set the value to tooltip

		Parameters:
			tooltip (string) : A string value
		"""
		self.__tooltip = tooltip
		self.__key_modified["tooltip"] = 1

	def get_created_source(self):
		"""
		The method to get the created_source

		Returns:
			string: A string value
		"""
		return self.__created_source

	def set_created_source(self, created_source):
		"""
		The method to set the value to created_source

		Parameters:
			created_source (string) : A string value
		"""
		self.__created_source = created_source
		self.__key_modified["created_source"] = 1

	def get_field_read_only(self):
		"""
		The method to get the field_read_only

		Returns:
			bool: A bool value
		"""
		return self.__field_read_only

	def set_field_read_only(self, field_read_only):
		"""
		The method to set the value to field_read_only

		Parameters:
			field_read_only (bool) : A bool value
		"""
		self.__field_read_only = field_read_only
		self.__key_modified["field_read_only"] = 1

	def get_validation_rule(self):
		"""
		The method to get the validation_rule

		Returns:
			string: A string value
		"""
		return self.__validation_rule

	def set_validation_rule(self, validation_rule):
		"""
		The method to set the value to validation_rule

		Parameters:
			validation_rule (string) : A string value
		"""
		self.__validation_rule = validation_rule
		self.__key_modified["validation_rule"] = 1

	def get_read_only(self):
		"""
		The method to get the read_only

		Returns:
			bool: A bool value
		"""
		return self.__read_only

	def set_read_only(self, read_only):
		"""
		The method to set the value to read_only

		Parameters:
			read_only (bool) : A bool value
		"""
		self.__read_only = read_only
		self.__key_modified["read_only"] = 1

	def get_association_details(self):
		"""
		The method to get the association_details

		Returns:
			string: A string value
		"""
		return self.__association_details

	def set_association_details(self, association_details):
		"""
		The method to set the value to association_details

		Parameters:
			association_details (string) : A string value
		"""
		self.__association_details = association_details
		self.__key_modified["association_details"] = 1

	def get_quick_sequence_number(self):
		"""
		The method to get the quick_sequence_number

		Returns:
			string: A string value
		"""
		return self.__quick_sequence_number

	def set_quick_sequence_number(self, quick_sequence_number):
		"""
		The method to set the value to quick_sequence_number

		Parameters:
			quick_sequence_number (string) : A string value
		"""
		self.__quick_sequence_number = quick_sequence_number
		self.__key_modified["quick_sequence_number"] = 1

	def get_custom_field(self):
		"""
		The method to get the custom_field

		Returns:
			bool: A bool value
		"""
		return self.__custom_field

	def set_custom_field(self, custom_field):
		"""
		The method to set the value to custom_field

		Parameters:
			custom_field (bool) : A bool value
		"""
		self.__custom_field = custom_field
		self.__key_modified["custom_field"] = 1

	def get_visible(self):
		"""
		The method to get the visible

		Returns:
			bool: A bool value
		"""
		return self.__visible

	def set_visible(self, visible):
		"""
		The method to set the value to visible

		Parameters:
			visible (bool) : A bool value
		"""
		self.__visible = visible
		self.__key_modified["visible"] = 1

	def get_length(self):
		"""
		The method to get the length

		Returns:
			int: A int value
		"""
		return self.__length

	def set_length(self, length):
		"""
		The method to set the value to length

		Parameters:
			length (int) : A int value
		"""
		self.__length = length
		self.__key_modified["length"] = 1

	def get_decimal_place(self):
		"""
		The method to get the decimal_place

		Returns:
			string: A string value
		"""
		return self.__decimal_place

	def set_decimal_place(self, decimal_place):
		"""
		The method to set the value to decimal_place

		Parameters:
			decimal_place (string) : A string value
		"""
		self.__decimal_place = decimal_place
		self.__key_modified["decimal_place"] = 1

	def get_view_type(self):
		"""
		The method to get the view_type

		Returns:
			ViewType: An instance of ViewType
		"""
		return self.__view_type

	def set_view_type(self, view_type):
		"""
		The method to set the value to view_type

		Parameters:
			view_type (ViewType) : An instance of ViewType
		"""
		self.__view_type = view_type
		self.__key_modified["view_type"] = 1

	def get_pick_list_values(self):
		"""
		The method to get the pick_list_values

		Returns:
			list: An instance of list
		"""
		return self.__pick_list_values

	def set_pick_list_values(self, pick_list_values):
		"""
		The method to set the value to pick_list_values

		Parameters:
			pick_list_values (list) : An instance of list
		"""
		self.__pick_list_values = pick_list_values
		self.__key_modified["pick_list_values"] = 1

	def get_multiselectlookup(self):
		"""
		The method to get the multiselectlookup

		Returns:
			dict: An instance of dict
		"""
		return self.__multiselectlookup

	def set_multiselectlookup(self, multiselectlookup):
		"""
		The method to set the value to multiselectlookup

		Parameters:
			multiselectlookup (dict) : An instance of dict
		"""
		self.__multiselectlookup = multiselectlookup
		self.__key_modified["multiselectlookup"] = 1

	def get_auto_number(self):
		"""
		The method to get the auto_number

		Returns:
			dict: An instance of dict
		"""
		return self.__auto_number

	def set_auto_number(self, auto_number):
		"""
		The method to set the value to auto_number

		Parameters:
			auto_number (dict) : An instance of dict
		"""
		self.__auto_number = auto_number
		self.__key_modified["auto_number"] = 1

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
