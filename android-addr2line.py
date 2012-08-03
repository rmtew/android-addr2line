#!/usr/bin/python                                                                                                                                                                                                                                                                
import sys
import re
import subprocess
import os

ADDR2LINE_BINARY=r"D:\Code\android-ndk-r8\toolchains\arm-linux-androideabi-4.4.3\prebuilt\windows\bin\arm-linux-androideabi-addr2line"
# full path to arm-linux-androideabi-addr2line
LIBRARY=r"D:\Code\games\Brogue-v1.6.4-Android\obj\local\armeabi"
# full path to your .so file

def main():
    print 'Paste the stack trace. CTRL-D to submit. CTRL-C to exit.'

    lines = []
    while True:
        try:
            line = raw_input()
        except KeyboardInterrupt:
            sys.exit()
        except EOFError:
            break
        lines.append(line)

    print ''

    addresses = []
    functions = []
    files = []

    for line in lines:
        address = get_address(line)
        if address is not None:
            library_file = get_library_file(line)
            if library_file:
                source = get_source_line(library_file, address)
                if source is not None:
                    addresses.append(address)
                    functions.append(source[0].strip())
                    files.append(source[1].strip())

    if len(addresses) == 0 or len(files) == 0:
        print 'No addresses found from %s.' % os.path.basename(LIBRARY)
        return

    for i in range(0, len(addresses)):
        print files[i] +":"+ functions[i]

def get_library_file(line):
    line = line.strip()
    if line.endswith(".so"):
        idx = line.rfind("/")
        if idx != -1:
            return line[idx+1:]

def get_address(line):
    search = re.search('#[0-9]{2} +pc +([0-9A-Fa-f]{8}) +/data', line)
    if search is None:
        return None
    else:
        return search.groups(1)[0]

def get_source_line(libfile, address):
    output = subprocess.check_output([ADDR2LINE_BINARY, '-C', '-f', '-e', os.path.join(LIBRARY, libfile), address]).split('\n')
    return (output[0], output[1])

if __name__ == '__main__':
    main()
