from os import path
import re


def read_file(file_name: str) -> list[str]:
    ''' Read file and return a list of string lines '''
    with open(file_name, 'r') as f:
        list_of_lines = f.readlines()
    return list_of_lines


def process_list_of_lines(list_of_lines: list[str]) -> list[list[str]]:
    ''' Process the list of string lines and return a list clean string lines
    Example: remove de \n and split by spaces, delete empty elements and delete 
    comments '''
    processed_lines = []
    for line in list_of_lines:
        line_without_comments = remove_comments(line)
        line_as_array = separete_line(line_without_comments)
        processed_lines.append(line_as_array)

    processed_lines = delete_empty_elements(processed_lines)

    return processed_lines


def remove_comments(line: str) -> str:
    ''' Remove comments in a line '''
    if '//' in line:
        index_value = line.index('//')
        line = line[0:index_value]
    return line


def separete_line(line: str) -> list[str]:
    result = line.split(',')  # Primero, separa la line por comas
    # Divide cada resultado por espacios y elimina espacios adicionales
    result = [item.strip() for item in result for item in item.split()]
    # Juntar elementos que estén entre paréntesis. Ej: ['MOV', 'A', '(', 'varA', ')'] -> ['MOV', 'A', '(varA)']
    result = join_elements_in_parenthesis(result)
    return result


def join_elements_in_parenthesis(line: list[str]) -> list[str]:
    ''' Join elements in parenthesis '''

    output_list = []
    parenthesis_content = []

    for item in line:
        if '(' in item and ')' in item:
            output_list.append(item)
        elif '(' in item:
            parenthesis_content.append(item)
        elif ')' in item:
            parenthesis_content.append(item)
            output_list.append(''.join(parenthesis_content))
            parenthesis_content = []
        else:
            if parenthesis_content:
                parenthesis_content.append(item)
            else:
                output_list.append(item)

    return output_list


def delete_empty_elements(lines: list[list[str]]) -> list[list[str]]:
    lines_without_spaces = []
    for line in lines:
        if len(line) != 0:
            lines_without_spaces.append(line)
    return lines_without_spaces


def get_format_lines(file_name: str) -> list[list[str]]:
    list_of_lines = read_file(path.join('codes', file_name))
    processed_lines = process_list_of_lines(list_of_lines)
    return processed_lines


if __name__ == "__main__":
    result = separete_line('MOV A,(10b)')
    print(result)
