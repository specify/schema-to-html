import sys

arguments = {
  'output': None,
  'format': 'html',
  'language': 'en',
}

for index, key in enumerate(sys.argv):
    if key.startswith('--'):
        stripped_key = key[2:]
        if stripped_key not in arguments:
            raise Exception(f'Unknown argument: {key}')
        if index+1 == len(sys.argv):
            raise Exception(f'No value specified for argument {key}')
        arguments[stripped_key] = sys.argv[index+1]

if arguments['format'] not in ['html', 'tsv']:
    raise Exception(
        'Only HTML and TSV output formats are supported'
    )
