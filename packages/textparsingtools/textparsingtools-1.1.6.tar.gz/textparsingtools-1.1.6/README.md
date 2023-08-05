# Text Parsing Tools

This is a collection of various functions to aid in parsing and organization of data stored in text files.

## Installation
You can install Text Parsing Tools from a command line via PyPI:

```
python3 -m pip install textparsingtools
```

This library was programmed using Python 3.8, and it has not been tested on older versions.

## How to use
Import the library and use its functions as needed. Here is a quick demo:

```
import text_parsing_tools

file_path = '<insert path here>'
input_file_name = 'Input file'
output_name = 'Output spreadsheet'

replacement_strings = [[' - ', '-'], ['   ', '  ']]

with open(file_path + input_file_name + '.txt', 'r') as input_file:
    file_lines = [recursively_replace(line , replacement_strings) for line in input_file.readlines()]

data_1 = get_text_data(file_lines, r"data_begin", r"data_end", 0, 1, data_begin_offset = 4)
data_2 = get_text_data(file_lines, r"data_2_begin", r"data_2_end", 0, 1, 2, 3, data_begin_offset = 5)

unique_names = []
[unique_names.append(row[0]) for row in data_1 if row[0] and row[0] not in unique_names]
[unique_names.append(row[0]) for row in data_2 if row[0] and row[0] not in unique_names]

data_1 = transpose_transcript_data(data_1, unique_names, empty_value = '=NA()')
data_2 = transpose_transcript_data(data_2, unique_names, empty_value = '=NA()')

combined_data = interleave_datasets(unique_names, data_1, data_2)

variables = ['Var 1', 'Var 2', 'Var 3', 'Var 4']
header = build_header(unique_names, variables)
write_excel_file(file_path + output_name, [combined_data], header)
```