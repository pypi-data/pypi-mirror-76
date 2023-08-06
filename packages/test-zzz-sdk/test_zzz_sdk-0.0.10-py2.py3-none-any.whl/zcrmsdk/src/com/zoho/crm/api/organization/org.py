from ..util import Model


class Org(Model):
	def __init__(self):
		self.__id = None
		self.__country = None
		self.__photo_id = None
		self.__city = None
		self.__description = None
		self.__mc_status = None
		self.__gapps_enabled = None
		self.__translation_enabled = None
		self.__street = None
		self.__alias = None
		self.__currency = None
		self.__state = None
		self.__fax = None
		self.__employee_count = None
		self.__zip = None
		self.__website = None
		self.__currency_symbol = None
		self.__mobile = None
		self.__currency_locale = None
		self.__primary_zuid = None
		self.__zia_portal_id = None
		self.__time_zone = None
		self.__zgid = None
		self.__country_code = None
		self.__phone = None
		self.__company_name = None
		self.__privacy_settings = None
		self.__primary_email = None
		self.__iso_code = None
		self.__license_details = None
		self.__key_modified = dict()

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

	def get_country(self):
		"""
		The method to get the country

		Returns:
			string: A string value
		"""
		return self.__country

	def set_country(self, country):
		"""
		The method to set the value to country

		Parameters:
			country (string) : A string value
		"""
		self.__country = country
		self.__key_modified["country"] = 1

	def get_photo_id(self):
		"""
		The method to get the photo_id

		Returns:
			string: A string value
		"""
		return self.__photo_id

	def set_photo_id(self, photo_id):
		"""
		The method to set the value to photo_id

		Parameters:
			photo_id (string) : A string value
		"""
		self.__photo_id = photo_id
		self.__key_modified["photo_id"] = 1

	def get_city(self):
		"""
		The method to get the city

		Returns:
			string: A string value
		"""
		return self.__city

	def set_city(self, city):
		"""
		The method to set the value to city

		Parameters:
			city (string) : A string value
		"""
		self.__city = city
		self.__key_modified["city"] = 1

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
		self.__description = description
		self.__key_modified["description"] = 1

	def get_mc_status(self):
		"""
		The method to get the mc_status

		Returns:
			bool: A bool value
		"""
		return self.__mc_status

	def set_mc_status(self, mc_status):
		"""
		The method to set the value to mc_status

		Parameters:
			mc_status (bool) : A bool value
		"""
		self.__mc_status = mc_status
		self.__key_modified["mc_status"] = 1

	def get_gapps_enabled(self):
		"""
		The method to get the gapps_enabled

		Returns:
			bool: A bool value
		"""
		return self.__gapps_enabled

	def set_gapps_enabled(self, gapps_enabled):
		"""
		The method to set the value to gapps_enabled

		Parameters:
			gapps_enabled (bool) : A bool value
		"""
		self.__gapps_enabled = gapps_enabled
		self.__key_modified["gapps_enabled"] = 1

	def get_translation_enabled(self):
		"""
		The method to get the translation_enabled

		Returns:
			bool: A bool value
		"""
		return self.__translation_enabled

	def set_translation_enabled(self, translation_enabled):
		"""
		The method to set the value to translation_enabled

		Parameters:
			translation_enabled (bool) : A bool value
		"""
		self.__translation_enabled = translation_enabled
		self.__key_modified["translation_enabled"] = 1

	def get_street(self):
		"""
		The method to get the street

		Returns:
			string: A string value
		"""
		return self.__street

	def set_street(self, street):
		"""
		The method to set the value to street

		Parameters:
			street (string) : A string value
		"""
		self.__street = street
		self.__key_modified["street"] = 1

	def get_alias(self):
		"""
		The method to get the alias

		Returns:
			string: A string value
		"""
		return self.__alias

	def set_alias(self, alias):
		"""
		The method to set the value to alias

		Parameters:
			alias (string) : A string value
		"""
		self.__alias = alias
		self.__key_modified["alias"] = 1

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
		self.__currency = currency
		self.__key_modified["currency"] = 1

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
		self.__state = state
		self.__key_modified["state"] = 1

	def get_fax(self):
		"""
		The method to get the fax

		Returns:
			string: A string value
		"""
		return self.__fax

	def set_fax(self, fax):
		"""
		The method to set the value to fax

		Parameters:
			fax (string) : A string value
		"""
		self.__fax = fax
		self.__key_modified["fax"] = 1

	def get_employee_count(self):
		"""
		The method to get the employee_count

		Returns:
			string: A string value
		"""
		return self.__employee_count

	def set_employee_count(self, employee_count):
		"""
		The method to set the value to employee_count

		Parameters:
			employee_count (string) : A string value
		"""
		self.__employee_count = employee_count
		self.__key_modified["employee_count"] = 1

	def get_zip(self):
		"""
		The method to get the zip

		Returns:
			string: A string value
		"""
		return self.__zip

	def set_zip(self, zip):
		"""
		The method to set the value to zip

		Parameters:
			zip (string) : A string value
		"""
		self.__zip = zip
		self.__key_modified["zip"] = 1

	def get_website(self):
		"""
		The method to get the website

		Returns:
			string: A string value
		"""
		return self.__website

	def set_website(self, website):
		"""
		The method to set the value to website

		Parameters:
			website (string) : A string value
		"""
		self.__website = website
		self.__key_modified["website"] = 1

	def get_currency_symbol(self):
		"""
		The method to get the currency_symbol

		Returns:
			string: A string value
		"""
		return self.__currency_symbol

	def set_currency_symbol(self, currency_symbol):
		"""
		The method to set the value to currency_symbol

		Parameters:
			currency_symbol (string) : A string value
		"""
		self.__currency_symbol = currency_symbol
		self.__key_modified["currency_symbol"] = 1

	def get_mobile(self):
		"""
		The method to get the mobile

		Returns:
			string: A string value
		"""
		return self.__mobile

	def set_mobile(self, mobile):
		"""
		The method to set the value to mobile

		Parameters:
			mobile (string) : A string value
		"""
		self.__mobile = mobile
		self.__key_modified["mobile"] = 1

	def get_currency_locale(self):
		"""
		The method to get the currency_locale

		Returns:
			string: A string value
		"""
		return self.__currency_locale

	def set_currency_locale(self, currency_locale):
		"""
		The method to set the value to currency_locale

		Parameters:
			currency_locale (string) : A string value
		"""
		self.__currency_locale = currency_locale
		self.__key_modified["currency_locale"] = 1

	def get_primary_zuid(self):
		"""
		The method to get the primary_zuid

		Returns:
			string: A string value
		"""
		return self.__primary_zuid

	def set_primary_zuid(self, primary_zuid):
		"""
		The method to set the value to primary_zuid

		Parameters:
			primary_zuid (string) : A string value
		"""
		self.__primary_zuid = primary_zuid
		self.__key_modified["primary_zuid"] = 1

	def get_zia_portal_id(self):
		"""
		The method to get the zia_portal_id

		Returns:
			string: A string value
		"""
		return self.__zia_portal_id

	def set_zia_portal_id(self, zia_portal_id):
		"""
		The method to set the value to zia_portal_id

		Parameters:
			zia_portal_id (string) : A string value
		"""
		self.__zia_portal_id = zia_portal_id
		self.__key_modified["zia_portal_id"] = 1

	def get_time_zone(self):
		"""
		The method to get the time_zone

		Returns:
			string: A string value
		"""
		return self.__time_zone

	def set_time_zone(self, time_zone):
		"""
		The method to set the value to time_zone

		Parameters:
			time_zone (string) : A string value
		"""
		self.__time_zone = time_zone
		self.__key_modified["time_zone"] = 1

	def get_zgid(self):
		"""
		The method to get the zgid

		Returns:
			string: A string value
		"""
		return self.__zgid

	def set_zgid(self, zgid):
		"""
		The method to set the value to zgid

		Parameters:
			zgid (string) : A string value
		"""
		self.__zgid = zgid
		self.__key_modified["zgid"] = 1

	def get_country_code(self):
		"""
		The method to get the country_code

		Returns:
			string: A string value
		"""
		return self.__country_code

	def set_country_code(self, country_code):
		"""
		The method to set the value to country_code

		Parameters:
			country_code (string) : A string value
		"""
		self.__country_code = country_code
		self.__key_modified["country_code"] = 1

	def get_phone(self):
		"""
		The method to get the phone

		Returns:
			string: A string value
		"""
		return self.__phone

	def set_phone(self, phone):
		"""
		The method to set the value to phone

		Parameters:
			phone (string) : A string value
		"""
		self.__phone = phone
		self.__key_modified["phone"] = 1

	def get_company_name(self):
		"""
		The method to get the company_name

		Returns:
			string: A string value
		"""
		return self.__company_name

	def set_company_name(self, company_name):
		"""
		The method to set the value to company_name

		Parameters:
			company_name (string) : A string value
		"""
		self.__company_name = company_name
		self.__key_modified["company_name"] = 1

	def get_privacy_settings(self):
		"""
		The method to get the privacy_settings

		Returns:
			bool: A bool value
		"""
		return self.__privacy_settings

	def set_privacy_settings(self, privacy_settings):
		"""
		The method to set the value to privacy_settings

		Parameters:
			privacy_settings (bool) : A bool value
		"""
		self.__privacy_settings = privacy_settings
		self.__key_modified["privacy_settings"] = 1

	def get_primary_email(self):
		"""
		The method to get the primary_email

		Returns:
			string: A string value
		"""
		return self.__primary_email

	def set_primary_email(self, primary_email):
		"""
		The method to set the value to primary_email

		Parameters:
			primary_email (string) : A string value
		"""
		self.__primary_email = primary_email
		self.__key_modified["primary_email"] = 1

	def get_iso_code(self):
		"""
		The method to get the iso_code

		Returns:
			string: A string value
		"""
		return self.__iso_code

	def set_iso_code(self, iso_code):
		"""
		The method to set the value to iso_code

		Parameters:
			iso_code (string) : A string value
		"""
		self.__iso_code = iso_code
		self.__key_modified["iso_code"] = 1

	def get_license_details(self):
		"""
		The method to get the license_details

		Returns:
			LicenseDetails: An instance of LicenseDetails
		"""
		return self.__license_details

	def set_license_details(self, license_details):
		"""
		The method to set the value to license_details

		Parameters:
			license_details (LicenseDetails) : An instance of LicenseDetails
		"""
		self.__license_details = license_details
		self.__key_modified["license_details"] = 1

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
