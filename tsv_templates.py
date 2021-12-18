# -*- coding: utf-8 -*-
"""Tiny TSV templates engine."""

import json

def deserialize(serialized):
    return map(lambda value: value, serialized.split('}{'))


def list_item(**_kwargs):
    return ''


def main(table_definitions, **_kwargs):
    return [
        'table_name',
        'field_name',
        'field_type',
        'field_length',
        'relationship_type'
        'relationship_table'
        'flags',
        'description'
    ]
    return table_definitions


def table_definition(
    table_id,
    table_definition_rows,
    table_relationships_rows,
    **_kwarg
):
    fields = deserialize(table_definition_rows)
    relationships = deserialize(table_relationships_rows)
    
def table_definition_row(**kwargs):
    return json.dumps(kwargs)

def table_relationships_rows(**kwargs):
    return json.dumps(kwargs)


tsv_templates = {
    'list_item': list_item,
    'main': main,
    'table_definition': table_definition,
    'table_definition_row': table_definition_row,
    'table_relationships_rows': table_relationships_rows,
}
