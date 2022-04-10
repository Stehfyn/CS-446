#@auth: @Stehfyn
#from fileinput import hook_encoded
import os, sys, subprocess
from typing import List

class Directory:
		def __init__(self, _path :str, _name :str):
			self.path = os.path.abspath(_path)
			self.name = _name
			self.files = list("")
			self.directories = []

			cur = os.path.abspath(os.curdir)
			os.chdir(self.path)
			init_list = ["mkdir", _name]
			subprocess.run(init_list)
			os.chdir(cur)
			
		def add_file(self, _file_name :str):
			cur = os.path.abspath(os.curdir)
			os.chdir(self.path + '/' + self.name)
			touch_list = ["touch", _file_name]
			subprocess.run(touch_list)
			self.files.append(_file_name)
			os.chdir(cur)
		
		def add_directory(self, _dir_name :str):
			cur = os.path.abspath(os.curdir)
			os.chdir(self.path + '/' + self.name)
			add = Directory(self.path + '/' + self.name, _dir_name)
			self.directories.append(add)
			os.chdir(cur)

		def __del__(self):
			#TODO: we can traverse our dir lists and explicitly call our __del__ 
			#we got the lazy handling here:
			try:
				cur = os.path.abspath(os.curdir)
				os.chdir(self.path)
				del_list = ["rm", "-r", self.name]	
				subprocess.run(del_list)
				print(del_list)
				os.chdir(cur)
			except Exception as inst:
				if type(inst) != FileNotFoundError:
					print(inst)
class Stats:
		def __init__(self):
			self.files = 0
			self.size = 0
			self.elapsed = 0
			
def main():
	print("main")
	single = construct_single(100)
	hierarchical = construct_hierarchical(10,100)
	#subprocess.run(["ls", "../.."])
	#subprocess.run(["ls", "../../" + single.name])
	subprocess.run(["ls", "../../" + hierarchical.name])
	for d in hierarchical.directories:
		subprocess.run(["ls", "../../" + hierarchical.name + '/' + d.name])
	s = traverse(single, visit)
	h = traverse(hierarchical, visit)

def construct_single(_files :int) -> Directory:
	home_dir = os.environ["HOME"]
	single = Directory(home_dir, "singleRoot")

	for x in range(1, _files + 1):
		path = single.path + '/' + single.name
		single.add_file("file" + str(x) + ".txt")
	return single

def construct_hierarchical(_dirs :int, _files :int) -> Directory:
	home_dir = os.environ["HOME"]
	hierarchical = Directory(home_dir, "hierarchicalRoot")

	if _files % _dirs != 0:
		raise Exception
	
	split = _files //_dirs

	for d in range(1, _dirs + 1):

		r = range(d*split-(split-1), d*split + 1)
		dir_name = "files" + str(list(r)[0]) + '-' + str(list(r)[len(list(r))-1])
		hierarchical.add_directory(dir_name)

		for x in r:
			hierarchical.directories[d-1].add_file("file" + str(x) + ".txt")

	return hierarchical

def visit(_dir :Directory):
	return

def traverse(_dir :Directory, _stats :Stats) -> Stats:
	if len(_dir.directories) > 0:
		for d in _dir.directories:
			s = traverse(d, _stats)
			_stats.files += s.files
			_stats.size += s.size
	for f in _dir.files:
    	s = os.stat(_dir.path + '/' + f)
	return

if __name__ == "__main__":
	try:
		main()
	except Exception as inst:
		print(inst)
