#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import sys

def main():
    init()

# Arguments parsing.
def init():
    args = sys.argv
    args = args[1:] # First element of args is the file name
    
    if len(args) == 0:
        # If no argument run rdmi_gen with default value (1..10).
        rdmi_gen()
    else:
        if args[0] == '-h' or args[0] == '--help':     
            print('rdmi allow you to print a range of numbers in random order.')
            print('')
            print('Usage:')
            print('    rdmi [-l <nb_min> <nb_max>]')
            print('    rdmi -h | --help')
            print('    rdmi --version')
            print('Options:')
            print('    -h --help  -> show this basic help menu.')
            print('    -l --limit -> Define range limit.')
            # If user set defined range, run rdmi_gen as a parameters.
        elif args[0] == '-l' or args[0] == '--limit':
            rdmi_gen(int(args[1]),int(args[2]))
        else:
            print('Unrecognised argument.')

# Function with default parameter if no parameter set.
def rdmi_gen(numb_a=1, numb_z=10):

    numbers = list(range(numb_a, numb_z+1))

    # Shuffle number position in the list.
    random.shuffle(numbers)

    print("Numbers from %s to %s in a random order : " % (numb_a, numb_z))

    # Output print the shuffle list.
    print(*numbers)

if __name__ == '__main__':
    main()
