#!/usr/bin/env python3
# v2018.05.11

import sys
import ruamel.yaml
import os

def modify(filename,var,val,node=None):
	yaml=ruamel.yaml.YAML()
	yaml.width=4096
	f=open(filename,"r")
	data=yaml.load(f.read())
	datamod=data
	if node:
		for n in node:
			datamod=datamod.get(n)
	datamod[var]=val
	f=open(filename, "w")
	yaml.dump(data, f)

def read(filename):
	# Cargar yaml en ordereddict
	import collections
	ruamel.yaml.representer.RoundTripRepresenter.add_representer(
	collections.OrderedDict, ruamel.yaml.representer.RoundTripRepresenter.represent_ordereddict)
	f=open(filename,"rt")
	yaml=f.read()
	yaml=yaml.replace("\t", "  ")
	data=ruamel.yaml.load(yaml, Loader=ruamel.yaml.Loader)
	return data

# Interpreta include: [ file1, file2 .. ]
def readparse(filename):
	data=read(filename)
	if data.get("yaml-include"):
		for f in data["yaml-include"]:
			if os.path.isfile(f):
				subdata=read(f)
				data.update(subdata)
			else:
				path=os.path.dirname(filename)
				f=path+os.path.sep+f
				if os.path.isfile(f):
					subdata=read(f)
					data.update(subdata)
		#data["include"]=None
		data.pop("yaml-include")
	return data
