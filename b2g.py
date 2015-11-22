#! /usr/bin/env python

import sys
import re
import pprint
import os

def check_file(argv):
    try:
        if argv[1]:
            return True
    except IndexError:
        print("No input file specified")
        return False


def create_dir(filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_palette_info(raw):
    n, info = raw
    result = {}
    result['number'] =  str(n).zfill(3)
    name = info[0][1]
    name_list = name.split("-")
    result['name_list'] = name_list
    result['name'] = result['number'] + " " +  " ".join([name_list[0], name_list[2]])

    result['filename'] = "/".join([name_list[2],
                                   name_list[1].zfill(2),
                                   name])
    result['palette'] = info
    return result

regs = {"comment":'^# *(.*)',
           "parts":
           {"title":'^\D+ palettes',
            "sub_title":'^[1-9] color palettes'}}

argv = sys.argv

result = []
if check_file(argv):
    with open(argv[1]) as fi:
        sub_result = []
        for line in fi:
            if not line.rstrip():
                continue
            comment = re.match(regs['comment'], line)
            if comment:
                m_line = comment.group(1)
                for part in regs['parts'].keys():
                    c_type = re.search(regs['parts'][part],m_line)
                    if c_type:
                        if sub_result:
                            result.append(sub_result)
                            sub_result = []
            else:
                split = line.rstrip().split(" = ")
                color = " ".join(split[1][:-1].split(","))
                name = split[0]
                sub_result.append((color,name))

for raw in enumerate(result):
    p = get_palette_info(raw)
    fn = p['filename']
    filename = "brewergpl/{0}.gpl".format(fn)
    create_dir(filename)
    header = "GIMP Palette\nName: {0}\nColumns: {1}\n#\n"
    header = header.format(p['name'], 1)
    print(filename)
    with open(filename,'w') as fo:
        fo.write(header)
        for color, comment in p['palette']:
            correct = re.match('.*[0-9]$', comment)
            if correct:
                parts = comment.split('-')
                parts = [parts[0], parts[2], parts[3]]
                name = "-".join(parts).lstrip().rstrip().replace('#','')
                color = color.lstrip().rstrip().replace('#','')
                line = "{0} {1}\n".format(color, name)
                fo.write(line)

