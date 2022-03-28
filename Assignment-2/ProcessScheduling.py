import os, sys
from os import path
from typing import List

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
