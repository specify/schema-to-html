# -*- coding: utf-8 -*-
"""Tiny templates engine wrapper."""

from string import Template

templates = [
    "list_item",
    "main",
    "table_definition",
    "table_definition_row",
    "table_relationships_rows",
]
file_path = Template("./html_templates/${name}.html")
html_templates = {}

for template in templates:
    with open(file_path.substitute(name=template)) as file:
        html_templates[template] = Template(file.read())
