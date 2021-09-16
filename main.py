# -*- coding: utf-8 -*-
"""Generate HTML file from Specify's datamodel."""

import xml.etree.ElementTree
from xml.dom import minidom
from string import Template
from pathlib import Path
import datetime
import os

data_model_xml_location = (
    "/Users/maxxxxxdlp/Downloads/specify_datamodel.xml"
)
schema_localization_xml_location = (
    "/Users/maxxxxxdlp/site/git/specify6/config/schema_localization.xml"
)
output_file = "schema.html"

current_directory = str(Path(__file__).parent) + "/"
templates = [
    "list_item",
    "main",
    "table_definition",
    "table_definition_row",
    "table_relationships_rows",
]
file_path = Template(current_directory + "html_templates/${name}.html")
html_templates = {}

for template in templates:
    with open(file_path.substitute(name=template)) as file:
        html_templates[template] = Template(file.read())

tree = xml.etree.ElementTree.parse(data_model_xml_location)
database = tree.getroot()

tree = minidom.parse(schema_localization_xml_location)
localization = tree.getElementsByTagName("container")

result = ""
list_of_tables = ""
table_definitions = ""
table_names = {}
languages = {
    "en": "English",
    "pt": "Portuguese",
    "pt_BR": "Portuguese (Brazilian)",
    "ru_RU": "Russian",
    "uk_UA": "Ukrainian",
}


def extract_strings(container):
    """Extract text from the <str> tag for each language into a dict.

    Args:
        container: <names> or <descs> element

    Returns:
        dict of strings
    """
    strings = {}
    for string in container.getElementsByTagName("str"):
        language = string.getAttribute("language")
        country = (
            f'_{string.getAttribute("country")}'
            if string.hasAttribute("country")
            and string.getAttribute("country")
            else ""
        )
        strings[f"{language}{country}"] = get_node_text(
            string.getElementsByTagName("text")[0]
        )

    # If localization is missing, use English variant
    if "en" in strings:
        for key in languages.keys():
            if key not in strings:
                strings[key] = strings["en"]

    return format_strings(strings)


def format_strings(strings):
    """Convert result of extract_strings (dict) into HTML string.

    Args:
        strings: output of extract_strings (dict)

    Returns:
        HTML string
    """
    return "\n".join(
        [
            f'<span class="language language-{key}">{strings[key]}</span>'
            for key in languages.keys()
            if key in strings
        ]
    )


def get_node_text(node):
    """Gen innerText of an XML node.

    Args:
        node: HTML node

    Returns:
        Inner text
    """
    for node in node.childNodes:
        if node.nodeType == node.TEXT_NODE:
            return node.data


def get_child(node, tag_name):
    """Analog of JS's node.getElementsByTagName(tag_name)[0].

    Args:
        node: parent node
        tag_name: tag name

    Returns:
        Returns first matching child element

    Raises:
        IndexError if unable to find the node
    """
    return [
        child
        for child in node.childNodes
        if child.nodeType != child.TEXT_NODE
        and child.tagName == tag_name
    ][0]


def find_node(nodes, attribute, value):
    """Search among nodes by attribute.

    Args:
        nodes: list of nodes
        attribute: attribute name
        value: attribute value

    Returns:
        First matched node

    Raises:
        IndexError if unable to find the node
    """
    return [
        node for node in nodes if node.getAttribute(attribute) == value
    ][0]


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

with open(
    os.path.join(current_directory, output_file), "w"
) as result_file:
    result_file.write(result)
