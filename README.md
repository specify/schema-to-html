# schema_to_html

Converts Specify's schema to an HTML page

## Requirements

You need to have Python 3.8+ and the following packages:

- xml.etree.ElementTree
- string
- pathlib
- datetime

## Configuration

Set `data_model_xml_location` variable in `main.py` to the location of
`specify_datamodel.xml` file.

Default location varies depending on the system:

- Mac OS: `/Applications/Specify/config/specify_datamodel.xml`
- Linux: `~/Specify/config/specify_datamodel.xml`
- Windows: `C:\Program Files\Specify\config\`

Similarly, set `schema_localization_xml_location` to the location of
"schema_localization.xml" file (you can get it from
[here](https://github.com/specify/specify6/blob/master/config/schema_localization.xml)
)

Then run the script

```zsh
python main.py
```

The resulting HTML file (`schema.html`) would be saved in the same directory as
`main.py`.

You will need to rerun `main.py` each time there is a schema change in Specify.
