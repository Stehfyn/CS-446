# 	@auth: Stephen Foster Mar '22 CS-446
# 	@repo: github.com/Stehfyn/CS-446
# 	@file: batchSchedulingComparison.py
# 	@vers: 1.0
#
# 	@impl: A Process class acts as our abstracted container of various simulation data (See class member "keys").
# 	A generalized simulation function (see simulate()) supports collecting the raw sim info regardless of simulation type.
# 	This is accomplished by utilizing anonymous lambda functions to sort a Process List by the the values of an individual
# 	Process' keys, listed from highest precedence to lowest. (see lines 106-113)
#
# 	@usage: cli: [python3] batchSchedulingComparison.py [input file] [simulation type]
#         	runtime: [input file] [simulation type]
#         	ex: python batchSchedulingComparison.py batch.txt FCFS
#
# 	@concl: FCFS as a solution is an easy implementation as it follows a FIFO behavior. This comes at the cost of throughput,
# 	as average turnaround and wait time tend to be high. SJN in contrast is the best approach to minimize waiting time, thus maximizing
# 	throughput. However, it's necessary for the CPU to know the Execution Time of a process for this algorithm to operate. Additionally,
# 	SJN is vulnerable to the behavior of starving lengthier processes of CPU time if shorter processes end up arriving frequently. This
# 	is not an issue in FCFS, as late arriving processes cannot influence the execution order of processes that have already entered the
# 	queue. PS is helpful as we're able to assign ordinal priority, and allow for higher priority work to occur first. This implementation 
# 	is less prone to starve lower priority processes as Arrival Time is the most deterministic in its behavior, however, this is still an
# 	effect to consider when Arrival Time isn't so effectual in other implementations. Additionally, though, our initial batchfile data does
# 	showcase this effect in contrast with its counterparts as PID 3, with a Burst Time of 50, significantly affected our turnaround and
# 	wait time averages when its priority became considered in scheduling. FCFS will likely be at its best use case in Batch systems, where
# 	jobs are queued in the order they arrive, and execute one after another until the job queue is empty. There's no user in this scenario 
# 	being inhibited by long-in-between response times. SJN will certainly beat out FCFS and PS in Interactive systems where a process' wait
# 	time is of upmost importance as its the key factor in fluidity of interactibility in user-focused applications. PS is most effective
# 	in systems where its warranted to assign ordinal priority amongst processes based on any number of factors, such as either static or 
# 	dynamic resource/timing requirements.

import os, sys
from os import path
from typing import List
from ProcessScheduling import *

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
