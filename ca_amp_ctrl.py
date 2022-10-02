#!/usr/bin/python3

import sys
import argparse
import libamp

# TBD need to adapt to new libamp!

# Build argument parser
parser = argparse.ArgumentParser(description="Control Cambridge Audio amplifiers.")
parser.add_argument('--pin', nargs='?', default=17, type=int)
parser.add_argument('--repeat', nargs='?', default=1, type=libamp.posint)
parser.add_argument('--device', nargs='?', default='CXA80', type=str)
parser.add_argument('command', nargs=1, choices=libamp.cmds['CXA80'].keys())
args = parser.parse_args()

command = args.command[0]
print("Sending '" + command + "' command to pin " + str(args.pin))

if args.repeat != 1:
    print(str(args.repeat) + " times")

libamp.execute(args.pin, args.device, command, args.repeat)

sys.exit(0)
