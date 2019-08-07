#!/usr/bin/python3
"""
Example of task for golf server.
This module has two functions,
first function generate arguments to submited program
second function generate string to compare STDOUT from submited code

If you still stuck, maybe pseudocode would be better for you:

>>> arguments = make_arguments()
>>> for argv in arguments:
>>>     result = do_it(argv)
>>>     stdout = execute_submited_code(argv)
>>>     assert result == stdout

This code is a standalone script too 
you can put in golf server or execute in terminal

for more rules please read file howto.html
"""


def make_arguments():
    """
        this function generate arguments (argv) to submited program 
        each record is a list with strings
        and will be executed by do_it function and submited code

        :return: List of arguments for argv
        :rtype: List[List[str]]
    """
    return [
        ['1', 'A'],  # result: A
        ['2', 'B'],  # result: BB
        ['3', 'C'],  # result: CCC
    ]


def do_it(*argv):
    """
        this function execute arguments (from make_arguments)
        and returns string who will be compared with 
        stdout from submited code

        :param argv: list of stringed arguments (argv)
        :type argv: List[str]
        :return: result to compare with 
        :rtype: str
    """
    count = int(argv[0])
    char = argv[1]
    return char * count + '\n'


if __name__ == "__main__":
    from sys import argv, stdout
    if len(argv) != 4:
        print('usage:', __file__, 'COUNT', 'CHAR')
        exit(-1)
    result = do_it(*argv[1:])
    stdout.write(result)
