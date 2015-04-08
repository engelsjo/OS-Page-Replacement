"""
Object that will hold some of the contents that a typical
pcb would hold, such as reference to its page table,
and also the size of the logical address space
"""

class pcb:
	def __init__(self):
		self.page_table = {}
		self.logical_addr_size = 0
		self.mem_references_made = 0
		self.number_of_faults = 0

	def update_size(self, size):
		if size > self.logical_addr_size:
			self.logical_addr_size = size

	def update_page_tbl(self, page, frame, time, resident_bit):
		"""
		@param page: The page of the process to update in page table
		@param frame: The frame that the page maps to in physical memory
		@param time: The time of the last reference
		@param resident_bit: flag that indicates if this page is in physical memory
		"""
		self.page_table[page] = [frame, time, resident_bit]
