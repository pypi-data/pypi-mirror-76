import sys
import os
import textparsingtools as tpt

file_path = 'C:/Data/'
input_file_name = 'example-transient'
output_name = 'Compiled transcript data'
replacement_strings = [[' - ', '-'], ['   ', '  '], ['Zone ','Zone']]
variables = ['Particles trapped', 'Mass flow initial (kg/s)', 'Mass flow final (kg/s)', 'Mass flow change (kg/s)']

os.chdir(file_path)

# Opens a data file and creates a list of each of its lines. Each line has replacements performed to allow whitespace-delimiting.
with open(file_path + input_file_name + '.txt', 'r') as input_file:
    file_lines = [tpt.recursively_replace(line , replacement_strings) for line in input_file.readlines()]

# Extracts particle fate data
# Arguments:
#   file_lines: list of lines of text
#   r"> report dpm-summary": raw regex string that indicates beginning of desired data
#   r"\n": raw regex string that indicates end of desired data
#   0, 1: column numbers of desired data (this argument is variable-length, so it could read "0", "0, 1", "0, 2", "0, 1, 2", etc.)
#   data_begin_offset = 4: optional keyword argument indicating that "> report dpm-summary" is found 4 lines before data begins
particle_fate_data = tpt.get_text_data(file_lines, r"> report dpm-summary", r"\n", 0, 1, data_begin_offset = 4)

# Extracts mass flow data
# Arguments:
#   file_lines: list of lines of text
#   r"  \(\*\)\- Mass Transfer Summary \-\(\*\) ": raw regex string that indicates begin of desired data (note that certan characters are escaped with backslashes)
#   r"\n": raw regex string that indicates end of desired data
#   0, 1, 2, 3: column numbers of desired data
#   data_begin_offset = 5: optional keyword argument indicating that data_begin_string is found 5 lines before data begins
mass_flow_data = tpt.get_text_data(file_lines, r"  \(\*\)\- Mass Transfer Summary \-\(\*\) ", r"\n", 0, 1, 2, 3, data_begin_offset = 5)

# Removes garbage rows that are all dashes
[mass_flow_data.remove(row) for row in mass_flow_data if row[0] and row[0].find('-') == 0]

# Finds all unique names found in the input file
unique_names = []
[unique_names.append(row[0]) for row in particle_fate_data if row[0] and row[0] not in unique_names]
[unique_names.append(row[0]) for row in mass_flow_data if row[0] and row[0] not in unique_names]
print('Names:',unique_names)

# Transposes the data from a list of rows to a list of columns
#   particle_fate_data, mass_flow_data: list to be transposed consisting of blocks of data separated by blank list elements
#   unique_names: list of names corresponding to each column
#   empty_value: value to be input if a given name is not found in a certain report
# For example, inputting this data (not a literal representation; actual data needs to be in list form):
# name1 1
# name2 8
#
# name1 3
# name3 9
#
# name4 2
# 
# with unique_names = ['name1', 'name2', 'name3', 'name4'], empty_value = '-'
# would result in:
# name1 name2 name3 name4
#   1     8     -     -
#   3     -     9     -
#   -     -     -     2
# where each column is a list. In list form, this would be:
# [[1, 3, '-'], [8, '-', '-'], ['-', '-', 2]]
# Note that the names are not included in the result. You must keep track of which name corresponds with which column.
particle_fate_data = tpt.transpose_transcript_data(particle_fate_data, unique_names, empty_value = '=NA()')
mass_flow_data = tpt.transpose_transcript_data(mass_flow_data, unique_names, empty_value = '=NA()')

# Combines the above datasets such that data for each name is adjacent. 
combined_data = tpt.interleave_datasets(unique_names, particle_fate_data, mass_flow_data)

# Builds the header and writes the Excel file
header = tpt.build_header(unique_names, variables)
[print(line) for line in header]
tpt.write_excel_file(file_path + output_name, [combined_data], header)