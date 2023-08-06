import datetime


class Constants(object):

    """
    This class uses the SDK constants name reference.
    """

    DATA_TYPE_ERROR = "DATA TYPE ERROR"

    ERROR = "error"

    REQUEST_METHOD_GET = "GET"

    REQUEST_METHOD_POST = "POST"

    REQUEST_METHOD_PUT = "PUT"

    REQUEST_METHOD_DELETE = "DELETE"

    OAUTH_HEADER_PREFIX = "Zoho-oauthtoken "

    AUTHORIZATION = "Authorization"

    API_NAME = "api_name"

    INVALID_ID_MSG = "The given id seems to be invalid."

    API_MAX_RECORDS_MSG = "Cannot process more than 100 records at a time."

    INVALID_DATA = "INVALID_DATA"

    CODE_SUCCESS = "SUCCESS"

    STATUS_SUCCESS = "success"

    STATUS_ERROR = "error"

    TAG = "tags"

    LEADS = "Leads"

    ACCOUNTS = "Accounts"

    CONTACTS = "Contacts"

    DEALS = "Deals"

    QUOTES = "Quotes"

    SALESORDERS = "SalesOrders"

    INVOICES = "Invoices"

    PURCHASEORDERS = "PurchaseOrders"

    PER_PAGE = "per_page"

    PAGE = "page"

    COUNT = "count"

    MORE_RECORDS = "more_records"

    MESSAGE = "message"

    CODE = "code"

    STATUS = "status"

    DETAILS = "details"

    TAXES = "taxes"

    DATA = "data"

    INFO = "info"

    FIELDS = 'fields'

    LAYOUTS = 'layouts'

    CUSTOM_VIEWS = 'custom_views'

    MODULES = 'modules'

    MODULE = 'module'

    RELATED_LISTS = 'related_lists'

    ORG = 'org'

    ROLES = 'roles'

    PROFILES = 'profiles'

    USERS = 'users'

    DOWNLOAD_FILE_PATH = "../../../../../../resources"

    USER_EMAIL_ID = "user_email_id"

    CURRENT_USER_EMAIL = "currentUserEmail"

    API_BASEURL = "apiBaseUrl"

    API_VERSION = "apiVersion"

    APPLICATION_LOGFILE_PATH = "applicationLogFilePath"

    ACTION = "action"

    DUPLICATE_FIELD = "duplicate_field"

    NO_CONTENT = "No Content"

    ATTACHMENT_URL = "attachmentUrl"

    GRANT_TYPE = "grant_type"

    GRANT_TYPE_AUTH_CODE = "authorization_code"

    ACCESS_TOKEN = "access_token"

    EXPIRES_IN = "expires_in"

    EXPIRES_IN_SEC = "expires_in_sec"

    REFRESH_TOKEN = "refresh_token"

    CLIENT_ID = "client_id"

    CLIENT_SECRET = "client_secret"

    REDIRECT_URL = "redirect_uri"

    TYPE_VS_DATATYPE = {
        "String": str,
        "List": list,
        "Integer": int,
        "HashMap": dict,
        "Map": dict,
        "Long": int,
        "Double": float,
        "Float": float,
        "DateTime": datetime.datetime
    }

    ZOHO_SDK = "X-ZOHO-SDK"

    SDK_VERSION = "3.0.0"

    CONTENT_DISPOSITION = "Content-Disposition"

    TOKEN_ERROR = "TOKEN ERROR"

    SAVE_TOKEN_ERROR = "Exception in saving tokens"

    INVALID_CLIENT_ERROR = "INVALID CLIENT ERROR"

    ERROR_KEY = 'error'

    GET_TOKEN_ERROR = "Exception in getting access token"

    MYSQL_HOST = "localhost"

    MYSQL_DATABASE_NAME = "zohooauth"

    MYSQL_USER_NAME = "root"

    MYSQL_PORT_NUMBER = "3306"

    GET_TOKEN_DB_ERROR = "Exception in getToken - DBStore"

    TOKEN_STORE = "TOKEN_STORE"

    DELETE_TOKEN_DB_ERROR = "Exception in delete_token - DBStore"

    SAVE_TOKEN_DB_ERROR = "Exception in save_token - DBStore"

    USER_MAIL = "user_mail"

    GRANT_TOKEN = "grant_token"

    EXPIRY_TIME = "expiry_time"

    GET_TOKEN_FILE_ERROR = "Exception in get_token - FileStore"

    SAVE_TOKEN_FILE_ERROR = "Exception in save_token - FileStore"

    DELETE_TOKEN_FILE_ERROR = "Exception in delete_token - FileStore"

    TYPE = "type"

    STREAM_WRAPPER_CLASS_PATH = 'zcrmsdk.src.com.zoho.crm.api.util.StreamWrapper'

    FIELD = "field"

    NAME = "name"

    INDEX = "index"

    CLASS = "class"

    ACCEPTED_TYPE = "accepted_type"

    GIVEN_TYPE = "given_type";

    TYPE_ERROR = "TYPE ERROR"

    VALUES = "values"

    ACCEPTED_VALUES = "accepted_values"

    UNACCEPTED_VALUES_ERROR = "UNACCEPTED VALUES ERROR"

    MIN_LENGTH = "min-length"

    MINIMUM_LENGTH = "minimum-length"

    MINIMUM_LENGTH_ERROR = "MINIMUM LENGTH ERROR"

    UNIQUE = "unique"

    FIRST_INDEX = "first-index"

    NEXT_INDEX = "next-index"

    UNIQUE_KEY_ERROR = "UNIQUE KEY ERROR"

    MAX_LENGTH = "max-length"

    MAXIMUM_LENGTH = "maximum-length"

    MAXIMUM_LENGTH_ERROR = "MAXIMUM LENGTH ERROR"

    REGEX = "regex"

    INSTANCE_NUMBER = "instance-number"

    REGEX_MISMATCH_ERROR = "REGEX MISMATCH ERROR"

    READ_ONLY = "read-only"

    IS_KEY_MODIFIED = 'is_key_modified'

    REQUIRED = "required"

    MANDATORY_VALUE_MISSING_ERROR = "MANDATORY VALUE MISSING ERROR"

    MANDATORY_KEY_MISSING_ERROR = "Value missing for mandatory key: "

    SET_KEY_MODIFIED = "set_key_modified"

    LIST_NAMESPACE = "List"

    MAP_NAMESPACE = "Map"

    HASH_MAP = "HashMap"

    STRUCTURE_NAME = "structure_name"

    KEYS = "keys"

    INTERFACE = "interface"

    RECORD_NAMESPACE = "zcrmsdk.src.com.zoho.crm.api.record.Record"

    RECORD_TYPE = "zcrmsdk.src.com.zoho.crm.api.record.record.Record"

    INVENTORY_LINE_ITEMS = "zcrmsdk.src.com.zoho.crm.api.record.InventoryLineItems"

    PRICINGDETAILS = "zcrmsdk.src.com.zoho.crm.api.record.PricingDetails"

    FIELD_FILE_NAMESPACE = "zcrmsdk.src.com.zoho.crm.api.record.FileDetails"

    REMINDAT_NAMESPACE = "zcrmsdk.src.com.zoho.crm.api.record.RemindAt"

    LINETAX = "zcrmsdk.src.com.zoho.crm.api.record.LineTax"

    REMINDER_NAMESPACE = "zcrmsdk.src.com.zoho.crm.api.record.Reminder"

    RECURRING_ACTIVITY_NAMESPACE = "zcrmsdk.src.com.zoho.crm.api.record.RecurringActivity"

    PARTICIPANTS = "zcrmsdk.src.com.zoho.crm.api.record.Participants"

    PACKAGE_NAMESPACE = "zcrmsdk.src.com.zoho.crm.api."

    USER_NAMESPACE = "zcrmsdk.src.com.zoho.crm.api.users.User"

    MODULE_NAMESPACE = "zcrmsdk.src.com.zoho.crm.api.modules.Module"

    LAYOUT_NAMESPACE = "zcrmsdk.src.com.zoho.crm.api.layouts.Layout"

    CHOICE_NAMESPACE = "zcrmsdk.src.com.zoho.crm.api.util.Choice"

    KEY_VALUES = "key_values"

    RECORD_CLASS_NAME = "Record"

    KEY_MODIFIED = "key_modified"

    CLASSES = "classes"

    LOGFILE_NAME = "sdk_logs.log"

    USER = "user"

    EXPECTED_TYPE = "expected-type"

    INITIALIZATION_ERROR = "INITIALIZATION ERROR"

    ENVIRONMENT = "environment"

    STORE = "store"

    TOKEN = "token"

    JSON_DETAILS_FILE_PATH = 'json_details.json'

    INITIALIZATION_ERROR = "Exception in initialization "

    EMAIL = "email"

    USER_ERROR = "USER ERROR"

    USER_INITIALIZATION_ERROR = "Error during User Initialization"

    EMAIL_REGEX = '^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$'

    STRING = "String"

    TOKEN_TYPE = "token_type"

    TOKEN_INITIALIZATION_ERROR = 'Exception in OAuthToken constructor'

    GRANT = "GRANT"

    REFRESH = "REFRESH"

    CONTENT_TYPE = 'Content-Type'

    STRING_NAMESPACE = 'String'

    BOOLEAN_NAMESPACE = 'Boolean'

    INTEGER_NAMESPACE = 'Integer'

    LONG_NAMESPACE = 'String'

    DOUBLE_NAMESPACE = 'Float'

    DATE_NAMESPACE = 'Date'

    DATETIME_NAMESPACE = 'DateTime'

    FILE_NAMESPACE = "zcrmsdk.src.com.zoho.crm.api.util.StreamWrapper"

    KEYS_TO_SKIP = ['Created_Time', 'Modified_Time', 'Created_By', 'Modified_By', 'Tag']

    PRODUCT_DETAILS = "Product_Details"

    PRICING_DETAILS = "Pricing_Details"

    PARTICIPANT_API_NAME = "Participants"

    INVENTORY_MODULES = ['Invoices', 'Sales_Orders', 'Purchase_Orders', 'Quotes']

    PRICE_BOOKS = "Price_Books"

    EVENTS = "Events"

    ACTIVITIES = "Activities"

    LAYOUT = "Layout"

    SUBFORM = "subform"

    LOOKUP = "lookup"

    SE_MODULE = "se_module"

    MODULEDETAILS = 'moduleDetails'

    MODULEPACKAGENAME = "modulePackageName"

    UNDERSCORE = "_"

    RELATED_LISTS = "Related_Lists"

    FIELD_DETAILS_DIRECTORY = "resources"

    NO_CONTENT_STATUS_CODE = 204

    API_NAME = "api_name"

    HREF = "href"

    API_EXCEPTION = "API_EXCEPTION"

    FIELDS_LAST_MODIFIED_TIME = "FIELDS-LAST-MODIFIED-TIME"

    LINE_TAX = "$line_tax"

    CANT_DISCLOSE = " ## can't disclose ## "

    URL = "URL"

    HEADERS = "HEADERS"

    PARAMS = "PARAMS"

    INITIALIZATION_SUCCESSFUL = "Initialization successful "

    INITIALIZATION_SWITCHED = "Initialization switched "

    IN_ENVIRONMENT = " in Environment : "

    FOR_EMAIL_ID = "for Email Id : "

    REFRESH_TOKEN_MESSAGE = "Access Token has expired. Hence refreshing."

    RESOURCE_PATH_ERROR = "EMPTY_RESOURCE_PATH"

    RESOURCE_PATH_ERROR_MESSAGE = "Resource Path MUST NOT be None/empty."

    SET_TO_CONTENT_TYPE = ["/crm/bulk/v2/read", "/crm/bulk/v2/write"]

    CONTENT_TYPE_HEADER = "Content-Type"

    LIST_KEY = "List"

    ATTACHMENT_ID = "attachment_id"

    FILE_ID = "file_id"

    DELETE_FIELD_FILE_ERROR = "Exception in deleting Current User Fields file : "

    DELETE_FIELD_FILES_ERROR = "Exception in deleting all Fields files : "

    DELETE_MODULE_FROM_FIELDFILE_ERROR = "Exception in deleting module from Fields file : "

    FILE_BODY_WRAPPER = 'FileBodyWrapper'

    EXCEPTION_IS_KEY_MODIFIED = "Exception in calling is_key_modified : "

    EXCEPTION_SET_KEY_MODIFIED = "Exception in calling set_key_modified : "





