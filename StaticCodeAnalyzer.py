import re
import sys
import os
import string


def indentation_check(text):
    indent = 0
    for c in text:
        if c == " ":
            indent += 1
        else:
            return indent % 4 == 0


def spaces(text):
    if 'def' in text:
        new_text = text.lstrip().replace('def', '')
        if len(new_text) - len(new_text.lstrip()) > 1:
            return True
    elif 'class' in text:
        new_text = text.replace(r'class', '')
        if len(new_text) - len(new_text.lstrip()) > 1:
            return True
    return False


def camel_case(text):
    if 'class' in text and text.lower() == text:
        return True
    return False


def snake_case(text):
    if 'def' in text and text.lower() != text:
        return True
    return False


def semicolon_check(text):
    counter = 0
    for c in text:
        if c == "#":
            return True
        if c in "\"'":
            counter += 1
        if c == ";" and counter % 2 == 0:
            return False
    return True


def inline_comments_check(text):
    if "#" in text:
        hash_index = text.index('#')
        if hash_index >= 2:
            return text[hash_index - 1] == " " and text[hash_index - 2] == " "
    return True


def todo_check(text):
    if "#" in text:
        hash_index = text.index('#')
        comment = text[hash_index:]
        return "TODO" in comment.upper()
    return False


def error_checker(file):
    open_file = open(file, 'r')
    blank_line = 0
    for i, line in enumerate(open_file):
        if len(line) > 79:
            print(f"{file}: Line {i + 1}: S001 Too long")

        if not indentation_check(line):
            print(f"{file}: Line {i + 1}: S002 Indentation is not a multiple of four")

        if not semicolon_check(line):
            print(f"{file}: Line {i + 1}: S003 Unnecessary semicolon after a statement")

        if not inline_comments_check(line):
            print(f"{file}: Line {i + 1}: S004 Less than two spaces before inline comments")

        if todo_check(line):
            print(f"{file}: Line {i + 1}: S005 TODO found")

        if line == "\n":
            blank_line += 1
        else:
            if blank_line > 2:
                print(f"{file}: Line {i + 1}: S006 More than two blank lines preceding a code line")
            blank_line = 0
        if spaces(line):
            print(f"{file}: Line {i + 1}: S007 Too many spaces after construction_name (def or class)")
        if camel_case(line):
            print(f"{file}: Line {i + 1}: S008 Class name class_name should be written in CamelCase")
        if snake_case(line):
            print(f"{file}: Line {i + 1}: S009 Function name function_name should be written in snake_case")


basepath = sys.argv[1]
files_dict = []
if '.py' in basepath:
    error_checker(basepath)
else:
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_file() and '.py' in entry.name:
                files_dict.append(basepath + os.sep + entry.name)
    for file in files_dict:
        error_checker(file)