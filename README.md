# schema_to_html

Converts Specify's schema to an HTML or TSV page

[See result](https://www.specifysoftware.org/specify-6-schema/)

## Requirements

You need to have Python 3.8+ and the following packages:

- xml.etree.ElementTree
- string
- pathlib
- datetime

## Generating output

Adjust the variables in `config.py` as needed, then run the script:

```zsh
python main.py --output ./schema.html --format html
```

Supported formats are HTML and TSV

If TSV format is chosen, you can also optionally specify the language:

```zsh
python main.py --output ./schema.tsv --format tsv --language en
```


The resulting HTML file (`schema.html`) would be saved in the same directory as
`main.py`.

You will need to rerun `main.py` each time there is a schema change in Specify.
