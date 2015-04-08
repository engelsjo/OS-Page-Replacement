'''
@author: Joshua Engelsma
@date: 03/26/2015
@version: 1.0
@summary: A tool used to visualize memory management using lru replacement
'''

import os
from datetime import datetime
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
		self.physical_memory = [-1 for i in range(15)]

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
		#create a new pcb for the process
		pcb_rec = pcb()
		pcb_rec.update_size(page_nbr)
		free_frame = self.get_frame()
		#add the page to physical memory
		self.physical_memory[free_frame] = (pid, page_nbr)
		#update the page table for the process
		pcb_rec.update_page_tbl(page_nbr, free_frame, datetime.now(), True)
		pcb_rec.mem_references_made += 1
		pcb_rec.number_of_faults += 1
		#add the pcb to the pcb records
		self.pcb_records[pid] = pcb_rec

	def _handle_first_page_ref(self, pid, page_nbr):
		"""
		@param pid: The pid of the process with a new page to load in
		@param page_nbr: The page number to load in
		"""
		pcb_rec = self.pcb_records[pid]
		pcb_rec.update_size(page_nbr)
		pcb_rec.mem_references_made += 1
		pcb_rec.number_of_faults += 1
		pcb_page_table = pcb_rec.page_table
		#PAGE FAULT!!!!
		free_frame = self.get_frame()
		#add the page to physical memory
		self.physical_memory[free_frame] = (pid, page_nbr)
		pcb_rec.update_page_tbl(page_nbr, free_frame, datetime.now(), True)
		#replace the updated pcb in the pcb records
		self.pcb_records[pid] = pcb_rec

	def _handle_page_reference(self, pid, page_nbr):
		"""
		@param pid: The pid of the page that is being referenced
		@param page_nbr: The page number that is being referenced
		This is a helper method to handle a page reference for an existing pcb record
		"""
		pcb_rec = self.pcb_records[pid]
		pcb_rec.update_size(page_nbr)
		pcb_rec.mem_references_made += 1
		pcb_page_table = pcb_rec.page_table
		if pcb_page_table[page_nbr][2] == True: #resident in RAM as of now
			#update the reference time
			pcb_rec.page_table[page_nbr][1] = datetime.now()
		else: #PAGE FAULT!!!!
			pcb_rec.number_of_faults += 1
			free_frame = self.get_frame()
			#add the page to physical memory
			self.physical_memory[free_frame] = (pid, page_nbr)
			pcb_rec.update_page_tbl(page_nbr, free_frame, datetime.now(), True)
			#replace the updated pcb in the pcb records
		self.pcb_records[pid] = pcb_rec

	def get_frame(self):
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
		Method navigates through the page tables of all of the processes.
		It finds the page in memory that was lru.
		It frees this frame from physical memory, adds the frame to the free list,
		and updates the resident bit of the corresponding page table entry to False.
		"""
		#grab the pid, page number, frame nbr, and time of all processes in memory
		frames_in_memory = []
		for pid in self.pcb_records:
			pcb = self.pcb_records[pid]
			process_pg_tbl = pcb.page_table
			for pg_nbr in process_pg_tbl:
				if process_pg_tbl[pg_nbr][2]: #resident bit
					frames_in_memory.append([pid, pg_nbr, process_pg_tbl[pg_nbr][0],process_pg_tbl[pg_nbr][1]])
		#find the oldest / lru of the frames in memory
		lru = frames_in_memory[0]
		for frame in frames_in_memory:
			if frame[1] < lru[1]:
				lru = frame
		#remove lru frame from physical memory
		self.physical_memory[lru[2]] = ""
		#add free frame to free list
		self.free_list.append(lru[2])
		#set the resident bit of the removed page to False
		self.pcb_records[lru[0]].page_table[lru[1]][2] = False

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
			if pid not in self.pcb_records:
				#we havent used this process yet 
				self._add_first_time_process(pid, page_nbr)
			elif page_nbr not in self.pcb_records[pid].page_table:
				#we havent loaded this page of the process in yet
				self._handle_first_page_ref(pid, page_nbr)
			else:
				#we already have a record for this process and page and need to manage it
				self._handle_page_reference(pid, page_nbr)
		self._printProgramExecution()
		
	def _printProgramExecution(self):
		for pid, pcb_r in self.pcb_records.iteritems():
			print("Process {} had a logical address space size of {}".format(pid, pcb_r.logical_addr_size))
			print("Process {} had {} total memory references made".format(pid, pcb_r.mem_references_made))
			print("Process {} had {} total memory faults".format(pid, pcb_r.number_of_faults))
		print("{}".format(self.physical_memory))



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


