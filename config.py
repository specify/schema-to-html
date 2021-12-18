# -*- coding: utf-8 -*-
"""Config. Refer to README.md for documentation"""

"""
Location of the specify_datamodel.xml file

Default location varies depending on the system:
- Mac OS: /Applications/Specify/config/specify_datamodel.xml
- Linux: ~/Specify/config/specify_datamodel.xml
- Windows: C:\Program Files\Specify\config\
"""
data_model_xml_location = (
    "/Users/maxxxxxdlp/Downloads/specify_datamodel.xml"
)

# Location of the schema_localization.xml file
# You can get it from here:
# https://github.com/specify/specify6/blob/master/config/schema_localization.xml
schema_localization_xml_location = (
    "/Users/maxxxxxdlp/site/git/specify6/config/schema_localization.xml"
)

# Which languages to output
languages = {
    "en": "English",
    "pt": "Portuguese",
    "pt_BR": "Portuguese (Brazilian)",
    "ru_RU": "Russian",
    "uk_UA": "Ukrainian",
}