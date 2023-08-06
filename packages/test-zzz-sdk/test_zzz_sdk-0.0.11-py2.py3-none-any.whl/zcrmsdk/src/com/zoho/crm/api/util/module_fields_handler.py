try:
    import os
    import json
    import logging
    import shutil
    from zcrmsdk.src.com.zoho.crm.api.util import Constants, Converter
    from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer

except Exception:
    import os
    import json
    import logging
    import shutil
    from .constants import Constants
    from .converter import Converter
    from ..initializer import Initializer


class ModuleFieldsHandler(object):
    logger = logging.getLogger('SDKLogger')

    @staticmethod
    def get_directory():
        return os.path.join(Initializer.get_initializer().resource_path, Constants.FIELD_DETAILS_DIRECTORY)

    @staticmethod
    def delete_fields_file():
        try:
            record_field_details_path = os.path.join(ModuleFieldsHandler.get_directory(), Converter.get_encoded_file_name())
            if os.path.exists(record_field_details_path):
                os.remove(record_field_details_path)
        except Exception as e:
            ModuleFieldsHandler.logger.info(Constants.DELETE_FIELD_FILE_ERROR + e.__str__())

    @staticmethod
    def delete_all_field_files():
        try:
            record_field_details_directory = ModuleFieldsHandler.get_directory()
            if os.path.exists(record_field_details_directory):
                shutil.rmtree(record_field_details_directory)
        except Exception as e:
            ModuleFieldsHandler.logger.info(Constants.DELETE_FIELD_FILES_ERROR + e.__str__())

    @staticmethod
    def delete_fields(module):
        try:
            record_field_details_path = os.path.join(ModuleFieldsHandler.get_directory(), Converter.get_encoded_file_name())
            if os.path.exists(record_field_details_path):
                record_field_details_json = Initializer.get_json(record_field_details_path)
                if module in record_field_details_json:
                    del record_field_details_json[module]

                with open(record_field_details_path, mode="w") as file:
                    json.dump(record_field_details_json, file)
                    file.flush()
                    file.close()
        except Exception as e:
            ModuleFieldsHandler.logger.info(Constants.DELETE_MODULE_FROM_FIELDFILE_ERROR + e.__str__())
