import pytest
import batchSchedulingComparison as target

def main():
	print("tests main")
	assert(target.showSimTypes() == None)

if __name__=="__main__":
	try:
		main()
		exit(0)
	except Exception as inst:
		print(type(inst))
		exit(1)
