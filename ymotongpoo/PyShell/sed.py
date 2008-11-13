#!/usr/bin/python
"""
@file : sed.py
@auther : ymotongpoo
@date : 2008.10.27
"""

import sys
import os
import re
import getopt

argvs = sys.argv
argc = len(argvs)


def usage(opt_args=''):
	print "usage : ./sed.py [-e script] [-f script_file] ... [file ...]"

####################################
# functions for -e style command
####################################
def find_separator(query):
	"""
	find separator '/' which is not escaped
	"""
	i = 0
	if query == []:
		print 'none'
		return
	else:
		try:
			i = query.index('/')
		except ValueError:
			return

		if query[i-1] != '\\':
			yield i
		for index in find_separator(query[i+1:]):
			yield index + i + 1


def parse_query(query):
	"""
	parse command like s/foo/bar/g into tuple
	"""
	index = []
	for i in find_separator(query):
		index.append(i)

	if len(index) == 3:
		command = query[:index[0]]
		target  = query[index[0]+1:index[1]]
		replace = query[index[1]+1:index[2]]
		flag    = query[index[2]+1:]
		return (command, target, replace, flag)
	else:
		print "ignore this option -- " + query
		sys.exit(1)


####################################
# functions for options
####################################
def expression_opt(opt_arg):
	return parse_query(opt_arg)
	

def file_opt(opt_arg):
	queries = []

	try:
		lines = open(opt_arg).readlines()
		for l in lines:
			queries.append(parse_query(l))

	except IOError:
		print "file not found"
		sys.exit(1)

	return queries


def version_opt(opt_arg=''):
	print "sed.py -- version 0.10"
	sys.exit()


def quiet_opt(opt_arg=''):
	sys.exit()


####################################
# process for each command in -e
####################################
def s_command(command, linex):
	return re.sub(command[1], command[2], line)


options = {'-n' : quiet_opt,
		   '-e' : expression_opt,
		   '-f' : file_opt,
		   '-V' : version_opt,
		   '-h' : usage,
		   '--help' : usage
		   }


#
# now -n option is not availble
# 
# 
def main():
	if argc < 3:
		sys.exit()
	else:
		try:
			opts, opt_args = getopt.getopt(argvs[1:], "Vhne:f:",
										   ["version", "help", "quiet", "expression=", "file="])
		except getopt.GetoptError:
			usage()
			sys.exit(2)

		queries = {} # dictionary of replace query

		# get options
		for o, v in opts:
			queries[o] = options[o](v)

		#print queries

		for target_file in opt_args:
			try:
				lines = open(target_file).readlines()
				f = open("_" + target_file, 'w')
			except IOError:
				print 'file not found'
				break
			
			if f:
				replace_queries = []
				# put together options
				if queries.has_key('-e'):
					replace_queries.append(queries['-e'])
				if queries.has_key('-f'):
					for q in queries['-f']:
						replace_queries.append(q)

				
				for line in lines:
					for q in replace_queries:
						if q[0] == 's':
							line = s_command(q, line)
					f.write(line)
					print line,
				
				f.close()

			else:
				print 'file not found'
				

			
if __name__ == '__main__':
	main()
else:
	sys.exit(1)
