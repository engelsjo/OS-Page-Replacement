'''
@author: Joshua Engelsma
@date: 03/26/2015
@version: 1.0
@summary: A tool used to visualize memory management using lru replacement
'''

import os

class memory_manager:
	def __init__(self):
		self.input_file = "{}/../input3a.data".format(os.path.abspath(os.path.dirname(__file__)))

	def _read_file(self, file_path):
		"""
		@param file_path: The path to the file we want to read in
		@return: a list with all the lines contained in the file
		"""
		file_contents = [line for line in open(file_path, 'r')]
		return file_contents

	def _convert_bin_to_decimal(self, bin_str):
		"""
		@param bin_str: a binary string that needs to be converted to decimal
		@return ret_val: an integer representation of the binary string
		"""
		ret_val = 0
		for idx, val in enumerate(reversed(bin_str)): #read through string backward
			curr_bit = int(val)
			ret_val += (curr_bit * pow(2, idx))
		return ret_val

	def manage(self):
		"""
		Main logic of management will occur here
		"""
		file_contents = self._read_file(self.input_file)
		for line in file_contents:
			line_contents = line.split()
			if len(line_contents) == 2:
				pid = line_contents[0]
				mem_bin_addr = line_contents[1]
				page_nbr = self._convert_bin_to_decimal(mem_bin_addr)
				print("{} needs to access page: {}".format(pid, page_nbr))
			else:
				raise Exception("Invalid file format. Must be 'pid    address'")


############################### Usage and Main ###############################
def usage():
    return """
    	You are not using the program correctly
    """

if __name__ == "__main__":
	manager = memory_manager()
	try:
		manager.manage()
	except Exception as e:
		print('############ Exception running page manager #############\n\n')
		print(e)
		print(usage())