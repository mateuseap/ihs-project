#!/usr/bin/python3

import sys

if len(sys.argv) < 2:
    print("Error: expected more command line arguments")
    print("syntax: %s </dev/device_file>"%sys.argv[0])
    exit(1)

while True:
    cmd = input("Open %s for Read or Write? [r/w]\nleave the script: [q]\n"%sys.argv[1])

    if cmd == 'r':
        fd = open(sys.argv[1], 'r')
        print("%s opened for read"%sys.argv[1])
        while True:
            cmd = input("How many bytes you want to read?\nclose the file: [c]\n")
            if cmd == 'c':
                fd.close()
                break
            else:
                retval = fd.read(int(cmd))
                print("red: %s"%retval)
    
    elif cmd == 'w':
        fd = open(sys.argv[1], 'w')
        print("%s opened for write"%sys.argv[1])
        while True:
            cmd = input("Type in what you want to write:\nclose the file: [c]\n")
            if cmd == 'c':
                fd.close()
                break
            else:
                retval = fd.write(cmd)
                print("wrote %s bytes"%int(retval))
    
    elif cmd == 'q':
        exit(0)
    
    else:
        print("input error")

