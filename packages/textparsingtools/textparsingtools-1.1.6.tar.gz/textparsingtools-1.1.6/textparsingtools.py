"""This module contains functions that allow parsing of whitespace-separated text files."""
import os
import re
import xlsxwriter

def build_header(names, variables):
    """Builds a header for a dataset where columns consist of repeating 
    variables for a list of names/categories.

    ### Parameters
    1. names : list
        - a list containing names of data categories
    2. variables : list
        - a list of repeating variables

    ### Returns
    - list
        - a nested list containing two header rows, where the first
          consists of <names> listed sequentially every n elements, and
          the second consists of cyclic repetition of n <variables>
    """
    header = [[],[]]
    for i in range(len(names)*len(variables)):
        if i % len(variables) == 0:
            # print(int(i/vars_per_name), len(names))
            header[0].append(names[int(i/len(variables))])
        else:
            header[0].append('')
        header[1].append(variables[i % len(variables)])
    return header

def trim_lines(lines, data_begin_str, data_end_str):
    """Trims a list of lines of text based on strings bounding desired content

    ### Parameters
    1. lines : list
        - a list containing each line of text
    2. data_begin_str : str
        - a string found in a line at the beginning of the desired data
    3. data_end_str: str
        - a string found in a line at the end of the desired data

    ### Returns
    - list
        - a list of lines of text, trimmed according to the specified
          bounds
    """
    # TODO: Rewrite this more efficiently, possibly copying from get_text_data.

    trimmed_lines = []
    reading_data = False
    line_number = 0
    while line_number < len(lines):
        # if debug and line_number % 1000 == 0:
            # print('Reading line:', file_lines[line_number])
        line = lines[line_number]

        if line.find(data_begin_str) != -1:
            reading_data = True
        elif line.find(data_end_str) != -1:
            reading_data = False

        if reading_data:
            trimmed_lines.append(line)

        line_number += 1
    return trimmed_lines

def get_dpm_flow_time(lines):
    """Creates a list of flow time for each dpm report in text from a Fluent transcript file

    ### Parameters
    1. lines : list
        - a list of lines of a Fluent transcript file
    
    ### Returns
    - list
        - a list of flow times corresponding with each dpm report
    """
    last_match = []
    flow_time_list = []
    
    time_regex = re.compile(r"Flow time = ((\d|\.)+)")
    report_regex = re.compile(r"-\n")

    for line in lines:
        match_flow_time = time_regex.search(line)
        match_report = report_regex.search(line)
        if match_flow_time:
            flow_time = match_flow_time.group(1)
            last_match = 'flow_time'
        if match_report and last_match == 'flow_time':
            flow_time_list.append(flow_time)
            last_match = 'report'
    
    return flow_time_list

def get_injection_groups(lines):
    """Creates a list of injection group numbers in dpm reports within text from a Fluent transcript file

    ### Parameters
    1. lines : list
        - a list of lines of a Fluent transcript file
    
    ### Returns
    - list
        - a list of injection group numbers in string format
    """
    injection_group_list = []

    regex = re.compile(r"injection-(\d+)")

    for line in lines:
        match = regex.search(line)
        if match and (len(injection_group_list) == 0 or not match.group(1) == injection_group_list[-1]):
            injection_group_list.append(match.group(1))
    
    return injection_group_list

def get_text_data(lines, data_begin_str, data_end_str, *column_numbers, separate_data = True, transpose_data=False, return_type=str, data_begin_offset=1):
    """Extracts whitespace-separated strings from lines of text

    Use www.regex101.com to test regex strings.

    ### Parameters 
    1. lines : list
        - a list containing each line of the text
    2. data_begin_str : str
        - a regex raw string found before data begins. Be sure to properly
          escape special characters.
    3. data_end_str : str
        - a regex raw string found in the line immediately after data ends. Be
          sure to properly escape special characters.
    4. *column_numbers : int
        - a variable-length list of column numbers (beginning with 0) pointing
          to desired data
    5. separate_data : bool, (default True)
        - a flag to indicate whether "chunks" of data (found between
          `data_begin_str` and `data_end_str`) should be demarkated with blank
          rows.
    6. transpose_data : bool, (default False)
        - a flag to indicate whether data should be transposed from a list of
          rows to a list of columns
    7. data_begin_offset : int, (default 1)
        - the number of lines to skip after data_begin_str before beginning
          reading data

    ### Returns
    - list
        - a list of lists of the data
    """
    # TODO: Add option to return number instead of string 
    # TODO: Remove blank row if only one chunk is read
    # TODO: Update documentation (and code if necessary) to indicate regex
    # string can occur anywhere, not just at start of line
    # TODO: Fix column number weirdness
    data = []
    reading_data = False

    lines_iter = iter(lines)
    for line in lines_iter:
        if re.search(data_begin_str, line):
            reading_data = True
            for _ in range(data_begin_offset-1):
                next(lines_iter)
            continue
        elif reading_data == True and re.match(data_end_str, line):
            reading_data = False
            # Appends a blank row to divide data
            if separate_data:
                data.append([[]]*len(column_numbers))
            continue

        if reading_data:
            # Uses regex to decompose line into whitespace-separated
            # values, then takes the columns corresponding to
            # column_numbers
            data.append([re.findall(r"(\S+)", line)[col] for col in column_numbers])
    
    data = [list(map(return_type, row)) for row in data]

    # NOTE: Possible inconsistent results with only 1 column
    if transpose_data:
        return [list(i) for i in zip(*data)]
    else:
        return data

def get_user_input(prompt, acceptable_answers):
    """Prompts and records user input within a list of acceptable answers.

    ### Parameters
    1. prompt : str
        - the prompt that will be displayed to the user
    2. acceptable_answers : list
        - a list of allowable answers
    
    ### Returns
    - str
        - a string containing the user's input
    """
    answer = input(prompt)
    while answer not in acceptable_answers:
        print('Please enter a response from the following list:', acceptable_answers)
        answer = input()
    return answer

def interleave_datasets(names, *data):
    """Shuffles multiple datasets together such that order is preserved.

    This function accepts multiple datasets which are ordered in groups of
    variables corresponding with an ordered list of names. For example, data
    could consist of lists [name1_var1], [name1_var2], [name2_var1],
    [name2_var2], etc. An input data list must have contain an equal number of
    variables for all values in names (in order). Different input data lists may
    have different numbers of variables (though each list must have a consistent
    number within), but each list must represent values of the same names in the
    same order. The function will output a single list containing, in order, all
    values for each variable. Continuing the above example, if a second data
    list were input containing [name1_var3], [name2_var3], etc., the output
    would be [name1_var1], [name1_var2], [name1_var3], [name2_var1],
    [name2_var2], [name2_var3], etc.

    ### Parameters
    1. names : list
        - a list of names/categories portrayed by each dataset. Only the length
          of this is used to determine how many elements to take from each
          dataset at a time.
    2. *data : list
        - lists of all datasets to combine

    ### Returns
    - list
        - a list of all combined data
    """
    out_data = []
    for index in range(len(names)):
        for dataset in data:
            var_count = int(len(dataset)/len(names))
            [out_data.append(cell) for cell in dataset[index*var_count:(index+1)*var_count]]
    return out_data

def recursively_replace(text, replacement_strings, max_iterations=100):
    """Performs recursive find-and-replace on input text.

    ### Parameters
    1. text : str
        - the text on which to perform replacement
    2. replacement_strings : list
        - a list of strings and their replacements, ordered like: [string1,
          replacement1, string2, replacement2,...]
    3. max_iterations : int, (default = 100)
        - the maximum iterations to perform for a single replacement.

    ### Returns
    - str
        - the result of the replacement operation
    """
        #print("Replacing '" + old_chars + "' with '" + new_chars + "' in string: '" + string + "'")
    for replacement_set in replacement_strings:
        # print(replacement_set)
        counter = 0
        old_chars = replacement_set[0]
        new_chars = replacement_set[1]
        
        if new_chars.find(old_chars) != -1:
            print('Error in recursively_replace: new_chars contains old_chars. Infinite loop will occur.')
        
        while text.find(old_chars) != -1:
            text = text.replace(old_chars, new_chars)
            counter += 1
            if counter > max_iterations:
                print('Error in recursively_replace: too many iterations. Input a larger value of max_iterations if you want to keep going.')
                break
    return text

def transpose_transcript_data(data, names, empty_value = ''):
    """Transposes data from a list of rows to a list of columns and adds entries for missing values.

    ### Parameters
    1. data : list
        - a nested list containing rows of data. The first element of each row
          contains a name or other independent variable identifying the data,
          and any number of subsequent elements can follow. Rows are grouped
          into 'blocks' separated by rows of [], where each block corresponds to
          a second independent variable. For example, each block could
          correspond to a certain position or time.
    2. names : list
        - an ordered list of names found in the first element of each row
    3. empty_value : str, (default = '')
        - the string that will be added wherever a given name is not found in a
          given block

    ### Returns
    - list
        - a list containing columns of the transposed data, where each row
          corresponds to one block. Each name in names will correspond to (in
          order) one column for each variable (the length of each row minus
          one). If a name found in data is omitted from names, its data will be
          discarded. If a name not found in data is included in names, its
          columns will be filled with empty_value. Any value not found in a
          given block will be represented by empty_value.
    """
    block = []
    transposed_data = []
    row_num = 0
    # Determines number of variables. Assumes one column represents name.
    var_count = len(data[0])-1
    # Create a column for number of names times number of variables per
    # name. Name is subtracted from the length of the row.
    [transposed_data.append([]) for i in range(var_count*len(names))]
    for row in data:
        print(row)
        if row[0]:
            block.append(row)
        if not row[0] or data.index(row) == len(data)-1:
            row_num += 1
            for row in block:
                col_index = names.index(row[0])
                [transposed_data[col_index*var_count + i - 1].append(row[i]) for i in range(1,len(row))]
            [col.append(empty_value) for col in transposed_data if len(col) < row_num]
            block = []
    
    return transposed_data

# Writes data to one or more sheets in a new or existing Excel file
# data: list of lists of lists, where the hierarchy is such: data[sheet][column][row]
# header: list of lists, where hierarchy is such: header[row][column]. This will be written to the top of each sheet.
# book_name: name of workbook to be created
# sheet_names: list of sheet names; dimensionality must agree with the top-level dimension of data
# overwrite: boolean to indicate whether an existing file with name book_name should be overwritten or appended to

def write_excel_file(book_name, data, header = [], sheet_names = [], overwrite = False, text_to_num = True):
    """Writes input data to one or more sheets in a new Excel file.

    ### Parameters
    1. book_name : str
        - the name of the new workbook
    2. data : list
        - a list of list of lists containing data. Hierarchy is
          data[sheet][row][column]
    3. header : list (default = [])
        - a list of lists describing the header to be added at the top of each
          sheet. Hierarchy is header[row][column] (note that row and column are
          reversed compared to data). If left empty, no header will be added.
    4. sheet_names : list (default = [])
        - a list of strings naming sheets in the new workbook. If number of
          sheets exceeds length of sheet_names, additional sheets will be named
          according to xlsxwriter default. If left blank, all sheets will be
          named default values.
    5. overwrite : bool, (default = False)
        - a boolean indicating whether an existing file should be overwritten
          without prompt. If overwrite is false, users will be asked whether
          they want to overwrite the existing file.
    6. text_to_num : bool, (default = True)
        - a boolean indicating whether text written to the workbook should be
          converted to float if possible

    ### Returns
    - none
    """
    if not overwrite and os.path.isfile(book_name + '.xlsx'):
        print()
        if str.upper(get_user_input('Warning: output file already exists. Do you want to overwrite? (Y/N)\n',['Y','N','y','n'])) == 'N':
            book_name = book_name + '_2'
            print('Output saved to ' + book_name + '.xlsx')


    workbook = xlsxwriter.Workbook(book_name + '.xlsx')

    # timestep_index_format = workbook.add_format({'num_format': '0'})
    # timestep_value_format = workbook.add_format({'num_format': '0.000'})
    # particle_fate_format = workbook.add_format({'num_format': '0'})
    # mass_flow_format = workbook.add_format({'num_format': '0.00E+00'})

    for sheet_num in range(len(data)):
        if sheet_names and len(sheet_names) > sheet_num:
            sheet = workbook.add_worksheet(sheet_names[sheet_num])
        else:
            sheet = workbook.add_worksheet()

        if header:
            header_rows = len(header)
        else:
            header_rows = 0

        for row_num in range(len(header)):
            row = header[row_num]
            for col_num in range(len(row)):
                sheet.write(row_num, col_num, header[row_num][col_num])

        for col_num in range(len(data[sheet_num])):
            col = data[sheet_num][col_num]
            for row_num in range(len(col)):
                # print(data[sheet_num][col_num][row_num+header_rows])
                cell_data = data[sheet_num][col_num][row_num]
                if text_to_num:
                    try:
                        cell_data = float(cell_data)
                    except: 
                        pass
                sheet.write(row_num + header_rows, col_num, cell_data)
                # print('Writing', data[sheet_num][col_num][row_num],'to cell',col_num,',',row_num)

    try:
        workbook.close()
        print('Workbook successfully closed')
    except:
            print('Error: could not write to ', book_name + '.xlsx.', 'Make sure the file is not open.')