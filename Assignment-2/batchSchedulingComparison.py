# @auth: Stephen Foster Mar '22 CS-446
# @file: batchSchedulingComparison.py
# @vers: 1.0
#
# @impl: A Process class acts as our abstracted container of various simulation data (See class member "keys").
# A generalized simulation function (see simulate()) supports collecting the raw sim info regardless of simulation type.
# This is accomplished by utilizing anonymous lambda functions to sort a Process List by the the values of an individual
# Process' keys, listed from highest precedence to lowest. (see lines 87-94)
#
# @usage: cli: [python3] batchSchedulingComparison.py [input file] [simulation type]
#         runtime: [input file] [simulation type]
#         ex: python batchSchedulingComparison.py batch.txt FCFS
#
# @concl: FCFS as a solution is an easy implementation as it follows a FIFO behavior. This comes at the cost of throughput,
# as average turnaround and wait time tend to be high. SJN in contrast is the best approach to minimize waiting time, thus maximizing
# throughput. However, it's necessary for the CPU to know the Execution Time of a process for this algorithm to operate. Additionally,
# SJN is vulnerable to the behavior of starving lengthier processes of CPU time if shorter processes end up arriving frequently. This
# is not an issue in FCFS, as late arriving processes cannot influence the execution order of processes that have already entered the
# queue. PS is helpful as we're able to assign ordinal priority, and allow for higher priority work to occur first. This implementation 
# is less prone to starve lower priority processes as Arrival Time is the most deterministic in its behavior, however, this is still an
# effect to consider when Arrival Time isn't so effectual in other implementations. Additionally, though, our initial batchfile data does
# showcase this effect in contrast with its counterparts as PID 3, with a Burst Time of 50, significantly affected our turnaround and
# wait time averages when its priority became considered in scheduling. FCFS will likely be at its best use case in Batch systems, where
# jobs are queued in the order they arrive, and execute one after another until the job queue is empty. There's no user in this scenario 
# being inhibited by long-in-between response times. SJN will certainly beat out FCFS and PS in Interactive systems where a process' wait
# time is of upmost importance as its the key factor in fluidity of interactibility in user-focused applications. PS is most effective
# in systems where its warranted to assign ordinal priority amongst processes based on any number of factors, such as either static or 
# dynamic resource/timing requirements. 

import os, sys
from os import path
from typing import List

def main():
	inputFile, simType = "", ""

	if len(sys.argv) != 3:
		showUsage(), showFileConvention(), showSimTypes()
		userInput = getInput()
		inputFile, simType = userInput[0], userInput[1]

	else:
		inputFile, simType = sys.argv[1], sys.argv[2]

	data = readFromFile(os.curdir, inputFile)
	procs = initProcesses(data)
	output = simulate(procs, simType)
	
	formatted = formatOutput(output)
	
	for line in formatted:
		print(line)
		
class Process:
	def __init__(self, _struc):
		self.keys = ["PID", 
					"Arrival Time", 
					"Burst Time", 
					"Priority",
					"Time Remaining",
					"Last Time",
					"Wait Times",
					"Completion Time"]
		self.data = {}

		for i, x in enumerate(_struc):
			self.data.update({self.keys[i]: x})

		self.data.update({"Time Remaining": self.data["Burst Time"]})

	def get(self, *args :str):
		if len(args) == 0:
			return self.data
		elif len(args) == 1:
			return self.data.get(args[0])
		else:
			raise Exception
	
	def set(self, *args) -> None:
		if len(args) == 2:
			self.data.update({args[0]: args[1]})
		else:
			raise Exception

def createStruc(_line :str) -> List[float]:
	nums = []
	_lines = _line.split(',')
	for x in _lines:
		nums.append(float(x))
	nums = checkFileConvention(nums)
	return nums
	
def initProcesses(_data :List[str]) -> List[Process]:
	procs = []
	for lines in _data:
		procs.append(Process(createStruc(lines)))
	return procs

class FileConventionError(Exception):
	pass

class SimTypeNotFoundError(Exception):
	pass

def firstComeFirstServedSort(_procs :List[Process]) -> List[Process]:
	return sorted(_procs, key=lambda p: (p.data["Arrival Time"], p.data["PID"]))

def shortestJobFirst(_procs :List[Process]) -> List[Process]:
	return sorted(_procs, key=lambda p: (p.data["Time Remaining"], p.data["PID"]))

def prioritySort(_procs :List[Process]) -> List[Process]:
	return sorted(_procs, key=lambda p: (p.data["Arrival Time"], p.data["Priority"], p.data["PID"]))

def averageTurnaround(_procs :List[Process]) -> float:
	sum = 0
	for p in _procs:
		sum += (p.get("Completion Time") - p.get("Arrival Time"))
	avg = sum / len(_procs)
	return round(avg, 2)

def averageWait(_procs :List[Process]) -> float:
	sum = 0
	for p in _procs:
		sum += (p.get("Completion Time") - p.get("Arrival Time") - p.get("Burst Time"))
	avg = sum / len(_procs)
	return round(avg, 2)

def simulate(_procs :List[Process], _sim_type :str) -> List[str]:
	print("Simulating", _sim_type + "...")
	_sim_type = checkSimType(_sim_type)
	procs_queue, sim_order, procs_bin = _procs, [], []

	t, last = 0, 0
	while len(procs_queue) > 0:
		available = []
		for p in procs_queue:
			if p.get("Arrival Time") <= t:
				available.append(p)
		
		current = _sim_type(available)[0]

		if len(sim_order) == 0:
			last = current.get("PID")

		if current.get("Burst Time") == current.get("Time Remaining"):
			current.set("Wait Times", [t - current.get("Arrival Time")])
			current.set("Last Time", t)

			sim_order.append(current.get("PID"))
	
		elif current.get("PID") != last:
			current.set("Wait Times", current.get("Wait Times") + [t - current.get("Last Time")])
			sim_order.append(current.get("PID"))
		
		current.set("Time Remaining", current.get("Time Remaining") - 1)
		current.set("Last Time", t+1)
		last = current.get("PID")
		
		if current.get("Time Remaining") == 0:
			current.set("Completion Time",  t+1)
			procs_bin.append(current)
			procs_queue.remove(current)

		t += 1

	return [sim_order, str(averageTurnaround(procs_bin)), str(averageWait(procs_bin))]

def getInput() -> List[str]:
	userInput = list("")
	while len(userInput) != 2:
		line = input("Please enter [input file] [simulation type]: ")
		userInput = line.split(' ')
	return userInput

def checkFileConvention(_nums :List[float]) -> List[float]:
	for num in _nums:
		if not num.is_integer():
			raise FileConventionError
	return _nums

def checkSimType(_sim_type :str) -> callable:
	simList = {"FCFS": firstComeFirstServedSort, 
				"ShortestFirst": shortestJobFirst, 
				"Priority": prioritySort}

	func = simList.get(_sim_type)
	if func == None:
		raise SimTypeNotFoundError
	return func

def showUsage() -> None:
	print("Usage:\n"
		+ "\tcli:"
		+ " [python3]"
		+ " " + os.path.basename(__file__)
		+ " [input file]"
		+ " [simulation type]"
		+ "\n\truntime:"
		+ " [input file]"
		+ " [simulation type]\n"
		+ "\tex: python batchSchedulingComparison.py batch.txt FCFS\n")
	return

def showSimTypes() -> None:
	print("Simulation Types:\n"
		+ "\tFCFS\n"
		+ "\tShortestFirst\n"
		+ "\tPriority\n")
	return

def showFileConvention() -> None:
	print("Input File Convention:\n"
		+ "\tEach line in an input file represents a process to be simulated.\n"
		+ "\tValues must be integers.\n"
		+ "\tUsage: [PID], [Arrival Time], [Burst Time], [Priority]\n"
		+ "\tex: 1, 1, 6, 2\n")
	return

def formatOutput(_output :List[str]) -> List[str]:
	sim_order, formatted = _output[0], []
	
	formatted.append("PID ORDER OF EXECUTION:")

	for pid in sim_order:
		formatted.append(str(int(pid)))
	
	formatted.append("Average Process Turnaround Time: " + _output[1])
	formatted.append("Average Process Wait Time: " + _output[2])

	return formatted

def readFromFile(_path :str, _in_file :str) -> List[str]:
	fin = open(_path + '/' + _in_file, 'r')
	lines = fin.readlines()
	fin.close()
	return lines

def outputToFile(_path :str, _out_file: str, _str :str) -> None:
	fout = open(_path + '/' + _out_file, 'a')
	fout.write(_str)
	fout.close()

def clearFile(_path :str, _out_file :str) -> None:
	fout = open(_path + '/' + _out_file, 'w')
	fout.write('')
	fout.close()

if __name__=="__main__":
	try:

		main(), exit(0)

	except Exception as inst:

		if type(inst) == FileNotFoundError:
			print("File Not Found\n")

		elif type(inst) == FileConventionError:
			print("File Convention Error\n")
			showFileConvention()

		elif type(inst) == SimTypeNotFoundError:
			print("Simulation Type Not Found.\n")
			showSimTypes()
		
		else:
			print(type(inst), inst.args, inst.with_traceback)

		print("Exiting..."), exit(1)