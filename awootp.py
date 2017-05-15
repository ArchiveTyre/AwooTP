#!/usr/bin/env python3

from sys import argv
from time import strftime
from os import path

pc = []
nl = None
hl = None
variables = {}
line = 1

class Line:
    def __init__(self, value):
        self.value = value
        self.next = None

    def print(self):
        if self.value == "":
            print ("")
        else:
            A = eval_line(self.value)
            if A:
                print (A)
        if self.next != None:
            self.next.print()

def unknown_var(var_name):
    global line
    return '[[[' + str(line) + ': UNKNOWN VARIABLE: "' + var_name +'"]]]'

def make_env():
    global variables
    variables["DATE"] = strftime("%d-%b %Y")
    variables["SPACE"] = " "

def eval_line(line):
    if line == "":
        return "";
    if line[0] == ":":
        return process_command(line[1:])
    else:
        return line

def process_command(full_command):
    global variables
    global hl
    global nl

    if full_command == "" or full_command[0] == "#":
        return None

    parts = full_command.split()
    command = parts[0]
    if len(parts) > 1:
        args = ' '.join(parts[1:])

    if command == "APPEND":
        process_line(eval_line(args))
        return None
    elif command == "VAR":
        var_name = eval_line(args).upper()
        return variables.get(var_name, unknown_var(var_name))
    elif command == "SET":
        variables[parts[1].upper()] =  eval_line(' '.join(parts[2:]))
        return None
    elif command == "INCLUDE":
        hl = nl
        process_file(path.expanduser(eval_line(args)))
        hl = hl.next
        print_file()
        return None
    elif command == "JOIN":
        result = []
        for var_request in parts[1:]:
            result.append(variables.get(var_request, unknown_var(var_request)))
        return ''.join(result)
    else:
        return "UNKNOWN COMMAND"

def process_line(line):
    global nl, hl
    newl = Line(line)
    if nl != None:
        nl.next = newl
    else:
        hl = newl
    nl = newl

def process_file(file_name):
    with open(file_name) as f:
        for line in f:
            process_line(line.rstrip("\n"))

def print_file():
    hl.print()

if len(argv) > 1:
    make_env()
    for f in argv[1:]:
        process_file(f)
        line+=1
    print_file()


