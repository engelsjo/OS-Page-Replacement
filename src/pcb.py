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

	def update_size(self, size):
		if size > self.logical_addr_size:
			self.logical_addr_size = size

	def update_page_tbl(self, page, frame):
		self.page_table[page] = frame
