# schema_to_html

Converts Specify's schema to an HTML or TSV page

[See result](https://www.specifysoftware.org/specify-6-schema/)

## Requirements

You need to have Python 3.8+, a checked out repository of [Specify 6](http://github.com/specify/specify6/) and an installed copy of Specify 6

## Configuration

Configuration options are described in [`./config.py`](https://github.com/specify/schema_to_html/blob/main/config.py)

Additionally, you might want to change the schema version number by editing [`./html_templates/main.html`](https://github.com/specify/schema_to_html/blob/d3d580e34fc742a3089ff912e395263f4e0d63cd/html_templates/main.html#L106-L114)

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
