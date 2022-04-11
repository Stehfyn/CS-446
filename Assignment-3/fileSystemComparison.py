# @auth: Stephen Foster Apr '22 CS-446
# @repo: github.com/Stehfyn/CS-446
# @file: fileSystemComparison.py
# @vers: 1.0
#
# @impl: Object-oriented approach to maintain readability. Originally sorting and positioning files alphanumerically happened inside 
# of get_statistics() which ate performance, and disproportionately affected single level directories at scale. I've changed the 
# implementation to better to highlight the average performance difference of traversing either kinds of directories.
#
# @usage: cli: [python3] fileSystemComparison.py
#         ex: python fileSystemComparison.py
#
# @concl: The similarity between average file sizes of Single-Level (SL) and Hiearchical (HL) is due to the fact that these days file
# sizes strictly refer to bytes not belonging to the metadata for the file, device, pipe, etc. Of course a files metadata could not be
# zero size, however this information is stored in the relevant inode. The reason why either directory (and any subdirectories) is/are 
# 4096 bytes a piece, is because that is the minimum overhead size of an inode (as it points to a single data block). Neither test case 
# exceeds the ability of a single data block, thus resulting in the similarity in size of directories. 
#
# UPDATE: After running the script on both a personal WSL environment vs. UNR's ubuntu webserver, it appears that the inode size 
# on the webserver is tuned differently. Some directories with the same amount of blank files are slightly different in size, in what
# I'm interpreting as the webserver having much smaller size data blocks, thus capturing (instead of aliasing) the differences in filename
# lengths, protections, indirections, etc. All directories went from exactly 4096 bytes in my personal WSL environment to roughly around 200 
# bytes on the webserver.
#
# The traversal time tends to lean towards SL, especially after changing the implementation to remove time bloat from ancillary functionality.
# This is due to the less indirection in searching an SL vs. a HL filesystem
# 
#    In a simple SL filesystem with arbitrarily long filenames and an arbitrary number of files, an emulation of filepaths would use a
# delimiting character to denote subdirectories. Using '#' as an example, a SL filesystem could emulate a desktop subdirectory by making
# desktop-intended files denoted through a delimited path: root#user#stehfyn#desktop#file.txt

import os, sys, subprocess
import re, stat

from typing import List
from time import process_time

def main():
    
    single = init_single_level_directory(100)
    hierarchical = init_hierarchical_level_directory(10, 10)

    print(single.get_statistics())
    write_tableu(single.path + single.name, "singleLevelFiles.txt", single)

    print(hierarchical.get_statistics())
    write_tableu(hierarchical.path + hierarchical.name, "hierarchicalFiles.txt", hierarchical)

    #force_delete_dir(single)
    #force_delete_dir(hierarchical)

class Statistics:
    data = {}
    keys = ["Name",
            "Number of Files",
            "Number of Directories",
            "Average File Size",
            "Average Directory Size (bytes)",
            "Traversal Time (ms)"]

    def __init__(self, _n, _f, _d, _tfs, _tds, _tt):
        #process_time() yields fractional second, thus t*1000 = # of ms
        vals = [_n, _f, _d, _tfs/_f if _f != 0 else 0, _tds/_d if _d != 0 else 0, round(_tt*1000, 8)] 
    
        for i, x in enumerate(self.keys):
            self.data.update({x:vals[i]})

    def __str__(self):
        s = ''
        s += self.data.get('Name') + '\n\n'
        for x in range(1, len(self.keys)):
            s += self.keys[x] + ': ' + f'{self.data.get(self.keys[x]):2}' + '\n'
        return s

class File:
    
    path = ''
    name = ''

    def __init__(self, _path, _name):
        self.path = os.path.abspath(_path) + '/'
        self.name = _name
        
        subprocess.getstatusoutput("touch " + self.path + self.name)

class Directory:

    path = ''
    name = ''

    files = []
    directories = []
    tableu = []

    def __init__(self, _path, _name):
            
        self.path = os.path.abspath(_path) + '/'
        self.name = _name

        if os.path.isdir(self.path + self.name):
            force_delete_dir(self)

        os.mkdir(self.path + self.name)
        
    def add_file(self, _file :str):
        self.files.append(File(self.path + self.name, _file))
        
    def make_directory(self, _dir :str):
        self.directories.append(Directory(self.path + self.name, _dir))

    def tableu_to_str(self):
        s = ''
        for dirs, sizes, files in self.tableu:
            if dirs != self.path + self.name:
                s += '\t'
            s += '{0:2} {1:3}'.format(dirs + '/', str(sizes))
            s += '\n'
            for f, sz in files:
                s += '\t\t' + '{0:2} {1:3}'.format(f, str(sz))
                s += '\n'
        return s

    def get_tableu(self):
        if len(self.tableu) == 0:
            self.get_statistics()
        return self.tableu

    def get_statistics(self):
        name, files, dirs, total_file_size, total_dir_size = "", 0, 0, 0, 0
        self.tableu.clear()

        start = process_time()
        for dirpath, dirnames, filenames in os.walk(self.path + self.name):
            file_and_size = []

            #sorted() here eats traversal time, a future impl would sort after
            #also, single level is greatly more likely eat time at scale, as
            #statistically speaking its bin size is 0 compared to hl's 10 in this use case!

            #for f in sorted(filenames, key=alpha_num_order):

            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    s = os.path.getsize(fp)
                    total_file_size += s
                    file_and_size.append((f,s))
                    files += 1
            
            dir_size = os.path.getsize(dirpath)

            if dirpath != self.path + self.name:
                self.tableu.append((os.path.basename(dirpath), dir_size, file_and_size))
                total_dir_size += dir_size
                dirs += 1
            else:
                self.tableu.append((dirpath, dir_size, file_and_size))
        end = process_time()

        if dirs == 0:
            name = "Single Level File System"
        else:
            name = "Hierarchical File System"
        return Statistics(name, files, dirs, total_file_size, total_dir_size, end-start)

def alpha_num_order(s :str):
    return ''.join([format(int(x), '05d') if x.isdigit()
                   else x for x in re.split(r'(\d+)', s)])
                   
def init_single_level_directory(_files :int) -> Directory:
    single = Directory(os.environ['HOME'], 'singleRoot')
    for x in range(_files):
        single.add_file("file" + str(x+1) + ".txt")
    return single
    
def init_hierarchical_level_directory(_dirs :int, _files :int) -> Directory:
    hierarchical = Directory(os.environ['HOME'], 'hierarchicalRoot')
    split = _files
    for d in range(_dirs):
        r = range((d+1)*split-(split-1), (d+1)*split + 1)
        dir_name = "files" + str(list(r)[0]) + '-' + str(list(r)[len(list(r))-1])
        hierarchical.make_directory(dir_name)
        for x in r:
            hierarchical.directories[d].add_file("file" + str(x) + ".txt")
    return hierarchical

def write_tableu(_path :str, _name :str, _dir :Directory) -> None:
    s = _dir.tableu_to_str()
    clearFile(_path, _name)
    outputToFile(_path, _name, s)

def force_delete_dir(_dir :Directory):
    cmd = "rm -rf " + _dir.path + _dir.name
    return subprocess.getstatusoutput(cmd)

def outputToFile(_path :str, _out_file: str, _str :str) -> None:
    fout = open(_path + '/' + _out_file, 'a')
    fout.write(_str)
    fout.close()

def clearFile(_path :str, _out_file :str) -> None:
    fout = open(_path + '/' + _out_file, 'w')
    fout.write('')
    fout.close()

if __name__=='__main__':
    try:
        main(), exit(0)
    except Exception as inst:
        print(inst), exit(1)