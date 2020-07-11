import xml.etree.ElementTree
from string import Template
from pathlib import Path
import datetime
import re

data_model_xml_location = '/Applications/Specify/config/specify_datamodel.xml'
output_file = 'schema.html'

path = str(Path(__file__).parent) + '/'
templates = ['list_item', 'main', 'table_definition', 'table_definition_row', 'table_relationships_rows']
file_path = Template(path + 'html_templates/${name}.html')
html_templates = {}

for template in templates:
    with open(file_path.substitute(name=template)) as file:
        html_templates[template] = Template(file.read().replace('\n', ''))

tree = xml.etree.ElementTree.parse(data_model_xml_location)
database = tree.getroot()

result = ''
list_of_tables = ''
table_definitions = ''
table_names = {}

format_table_name = re.compile(r'(?<!^)(?=[A-Z])')

for table in database:

    table_id = table.attrib['table']
    classname = table.attrib['classname']
    table_name = table_id

    fields = ''
    relationships = ''

    for field in table:

        if field.tag == "id":
            table_name = field.attrib['column'][0:-2]

        elif field.tag == "field":

            flags = []

            if field.attrib['required'] == 'true':
                flags.append('Required')

            if field.attrib['unique'] == 'true':
                flags.append('Unique')

            if field.attrib['indexed'] == 'true':
                flags.append('Indexed')

            flags = ' '.join(flags)

            if 'description' in field.attrib:
                description = field.attrib['description']
            else:
                description = ''


            if 'length' in field.attrib:
                length = field.attrib['length']
            else:
                length = ''

            fields += html_templates['table_definition_row'].substitute(name=field.attrib['column'],
                                                                        type=field.attrib['type'],
                                                                        length=length,
                                                                        description=description,
                                                                        flags=flags)

        elif field.tag == "relationship":
            relationships += html_templates['table_relationships_rows'].substitute(type=field.attrib['type'],
                                                                                   name=field.attrib['classname'],
                                                                                   target_table=field.attrib[
                                                                                       'relationshipname'])

    table_name = format_table_name.sub(' ', table_name).replace('D N A', 'DNA').replace('Dna', 'DNA')

    table_names[classname] = table_name

    list_of_tables += html_templates['list_item'].substitute(table_id=table_id,
                                                             table_name=table_name)

    table_definitions += html_templates['table_definition'].substitute(table_id=table_id,
                                                                       table_name=table_name,
                                                                       table_definition_rows=fields,
                                                                       table_relationships_rows=relationships)

js_list_of_tables = ''

while True:
    try:
        [classname, table_name] = table_names.popitem()
        js_list_of_tables += "'{}':'{}',".format(classname, table_name)
    except KeyError:
        break

date_generated = datetime.date.today()
result = html_templates['main'].substitute(date_generated=date_generated,
                                           list_of_tables=list_of_tables,
                                           table_definitions=table_definitions,
                                           js_list_of_tables=js_list_of_tables)

with open(path + output_file, "w") as result_file:
    result_file.write(result)
