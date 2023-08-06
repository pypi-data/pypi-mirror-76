#!/usr/bin/env python
import sys
sys.path.append("/omx") #This path will be bound to the nbx folder in run.sh
import numpy as np
from numpy import *

from nbx.pspace import ParameterSpace, Axis

import os
from pathlib import Path
import argparse
parser = argparse.ArgumentParser(description='Wraps an experiment...')
parser.add_argument('--job-id', dest="job_id", default=0, type=int)
parser.add_argument('--task-id', dest="task_id", default=0, type=int)
parser.add_argument('--results-dir', dest="results_dir", default=Path(__file__).parent/'results', type=str)

sweep_params = ParameterSpace([
	Axis("x", [0,1,2,3,4])
])

def print_args(arg_dict):
	print(f"**nbx**\nCalling main...")
	for k,v in arg_dict.items():
		print(f"\t{k}: {v}")


def run(x=0, y=0, task_id=0, results_dir="./"):
	"""
	This is an auto-generated function 
	based on the jupyter notebook 

	> om2.ipynb
	
	Don't judge, it might look ugly.
	"""
	print_args(locals())


	#nbx

	

	

	

	

	    

	

	

	#watch

	z = 1
	#nbx

	print("some result")

	print("\n**nbx**\nExperiment finished.")


if __name__ == '__main__':
	args = parser.parse_args()
	j  = args.job_id
	t  = args.task_id
	rd = Path(args.results_dir)/f"{t}"

	os.makedirs(rd, exist_ok=True)

	xargs = sweep_params[t-1]
	run(**xargs, task_id=t, results_dir=rd)