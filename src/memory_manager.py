'''
@author: Joshua Engelsma
@date: 03/26/2015
@version: 1.0
@summary: A tool used to visualize memory management using lru replacement
'''

import os
from pcb import pcb

class memory_manager:
	def __init__(self):
		#path to input file to read in
		self.input_file = "{}/../input3a.data".format(os.path.abspath(os.path.dirname(__file__)))
		#pcb records for processes
		self.pcb_records = {}
		#list of free frames available...defaults to all 16 free
		self.free_list = [i for i in range(15)]
		#structure containing the contents of physical memory
		self.physical_memory = []

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

	def _add_first_time_process(self, pid, page_nbr):
		"""
		@param pid: The pid that is being used for the first time 
		@param page_nbr: The page number the first time process is referencing
		This is a helper method to manage a process running for first time
		"""
		pcb_rec = pcb()
		pcb_rec.logical_addr_size = page_nbr
		free_frame = get_frame()
		pcb_rec.page_table[page_nbr] = free_frame
		pcb_rec.mem_references_made += 1
		self.pcb_records[pid] = pcb_rec

	def get_frame():
		"""
		Method that will look in free list, otherwise remove, and return a frame
		"""
		if len(self.free_list) != 0:
			return self.free_list.pop(0)
		else:
			#we have to boot lru add frame to free list, and return it
			self.replace_by_lru()
			return self.free_list.pop(0)

	def replace_by_lru(self):
		"""
		TODO: implement this bad boy
		"""


	def manage(self):
		"""
		Main logic of management will occur here
		"""
		file_contents = self._read_file(self.input_file)
		for line in file_contents: #parse the data file
			line_contents = line.split()
			if len(line_contents) == 2: #retrieve and format the pid and page number
				pid = line_contents[0]
				mem_bin_addr = line_contents[1]
				page_nbr = self._convert_bin_to_decimal(mem_bin_addr)
				print("{} needs to access page: {}".format(pid, page_nbr))
			else:
				raise Exception("Invalid file format. Must be 'pid    address'")
			if pid not in self.pcb_records: #we havent used this process yet
				self._add_first_time_process(pid, page_nbr)
			else: #we already have a record for this process and need to update
				calling_process = self.pcb_records[pid]
				calling_process.update_size(page_nbr)
				calling_process.mem_references_made += 1
				self.pcb_records[pid] = calling_process
		for pid, pcb_r in self.pcb_records.iteritems():
			print("Process {} had a logical address space size of {}".format(pid, pcb_r.logical_addr_size))
			print("Process {} had {} total memory references made".format(pid, pcb_r.mem_references_made))




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