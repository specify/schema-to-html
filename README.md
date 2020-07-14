# schema_to_html
Converts Specify's schema to an HTML page

# Requirements
You need to have Python 3.8+ and the following packages:
- xml.etree.ElementTree
- string
- pathlib
- datetime
- re

# How to run
Before you can run the script, you should specify the location of your `specify_datamodel.xml` file

In order to do that, change the value of `data_model_xml_location`  inside of `main.py`

The default location for that file vary depending on your system:
- Mac OS: `/Applications/Specify/config/specify_datamodel.xml`
- Linux: `~/Specify/config/specify_datamodel.xml`
- Windows: `C:\Program Files\Specify\config\`

After that, you can run the script by executing the following command in your terminal:
```
python3 main.py
```

The resulting HTML file would be saved in the same directory under the name `schema.html`

You will need to rerun `main.py` each time there is a schema change in Specify
