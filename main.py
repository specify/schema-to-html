# -*- coding: utf-8 -*-
"""Generate HTML file from Specify's datamodel."""

import xml.etree.ElementTree
from xml.dom import minidom
import datetime

from config import data_model_xml_location, schema_localization_xml_location, \
    output_location, languages
from templates import html_templates
from utils import extract_strings, get_child, find_node


tree = xml.etree.ElementTree.parse(data_model_xml_location)
database = tree.getroot()

tree = minidom.parse(schema_localization_xml_location)
localization = tree.getElementsByTagName("container")

result = ""
list_of_tables = ""
table_definitions = ""
table_names = {}


for table in database:

    table_id = table.attrib["table"]
    classname = table.attrib["classname"]

    localization_table = find_node(localization, "name", table_id)

    table_name = extract_strings(get_child(localization_table, "names"))
    table_description = extract_strings(
        get_child(localization_table, "descs")
    )
    field_localizations = localization_table.getElementsByTagName(
        "items"
    )[0].getElementsByTagName("desc")

    fields = ""
    relationships = ""

    for field in table:

        if field.tag not in ["field", "relationship"]:
            continue

        try:
            field_localization = find_node(
                field_localizations,
                "name",
                field.attrib[
                    "name"
                    if field.tag == "field"
                    else "relationshipname"
                ],
            ).getElementsByTagName("descs")[0]
            description = extract_strings(field_localization)
        except IndexError:
            description = ""

        if field.tag == "field":

            flags = []

            if field.attrib["required"] == "true":
                flags.append("Required")

            if field.attrib["unique"] == "true":
                flags.append("Unique")

            if field.attrib["indexed"] == "true":
                flags.append("Indexed")

            flags = " ".join(flags)

            if "length" in field.attrib:
                length = field.attrib["length"]
            else:
                length = ""

            fields += html_templates["table_definition_row"].substitute(
                name=field.attrib["column"],
                type=field.attrib["type"],
                length=length,
                description=description,
                flags=flags,
            )

        elif field.tag == "relationship":
            relationships += html_templates[
                "table_relationships_rows"
            ].substitute(
                type=field.attrib["type"],
                name=field.attrib["classname"],
                target_table=field.attrib["relationshipname"],
                description=description,
            )

    table_names[classname] = {"id": table_id, "name": table_name}

    list_of_tables += html_templates["list_item"].substitute(
        table_id=table_id, table_name=table_name
    )

    table_definitions += html_templates["table_definition"].substitute(
        table_id=table_id,
        table_name=table_name,
        table_description=table_description,
        table_definition_rows=fields,
        table_relationships_rows=relationships,
    )

date_generated = datetime.date.today()
result = html_templates["main"].substitute(
    date_generated=date_generated,
    list_of_tables=list_of_tables,
    table_definitions=table_definitions,
    table_names=table_names,
    languages=languages,
)

with open(output_location, "w") as result_file:
    result_file.write(result)
