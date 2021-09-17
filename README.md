# schema_to_html

Converts Specify's schema to an HTML page

## Requirements

You need to have Python 3.8+ and the following packages:

- xml.etree.ElementTree
- string
- pathlib
- datetime

## Generating HTML file

Adjust the variables in `config.py` as needed, then run the script:

```zsh
python main.py
```

The resulting HTML file (`schema.html`) would be saved in the same directory as
`main.py`.

You will need to rerun `main.py` each time there is a schema change in Specify.
