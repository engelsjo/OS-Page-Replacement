from Tkinter import *
from _tkinter import *
import ttk as ttk
from memory_manager import memory_manager
import sys
from time import sleep

########################   Create Instance of Model   ###################
manager = memory_manager()

#### place global vars here
table_labels = []
buttons = {}
process_tables_labels = {}
process_table_frames = []

########################   Controller methods for updating view #########

def update_pmemory_tbl():
	"""
	function that updates the physical memory table
	"""
	for i, frame in enumerate(manager.physical_memory):
		if frame != -1:
			if i < 10:
				if frame[1] < 10:
					table_labels[i]['text'] = "{}:             {}         {}".format(i, frame[0], frame[1])
				else:
					table_labels[i]['text'] = "{}:             {}       {}".format(i, frame[0], frame[1])
			else:
				if frame[1] < 10:
					table_labels[i]['text'] = "{}:           {}         {}".format(i, frame[0], frame[1])
				else:
					table_labels[i]['text'] = "{}:           {}       {}".format(i, frame[0], frame[1])

def update_page_tables():
	"""
	function that updates the page tables
	"""
	for pcb in manager.pcb_records:
		page_table = manager.pcb_records[pcb].page_table
		for page, page_info in sorted(page_table.iteritems()):
			if page > 9 and page_info[0] > 9:
				row_text = "{}:           {}       {}".format(page, page_info[0], page_info[2])
			elif page > 9:
				row_text = "{}:           {}         {}".format(page, page_info[0], page_info[2])
			elif page_info[0] > 9:
				row_text = "{}:             {}       {}".format(page, page_info[0], page_info[2])
			else:
				row_text = "{}:             {}         {}".format(page, page_info[0], page_info[2])
			process_tables_labels[pcb][page]['text'] = row_text

def run_to_next_step():
	"""
	function that executes the next reference in the data file
	"""
	if manager.curr_ref_index == (len(manager.file_contents) - 1):
		buttons['Complete']['state'] = DISABLED
		buttons['Next']['state'] = DISABLED
	#update the model
	manager.runToNextStep()
	#update the view
	update_pmemory_tbl()
	update_page_tables()

def run_to_completion():
	"""
	function that executes the entire data file
	""" 
	#update the model
	manager.runToCompletion()
	#update the view
	update_pmemory_tbl()
	update_page_tables()
	#disable buttons
	for btn in buttons.keys():
		if btn != "Quit" and btn != "Reset":
			buttons[btn].config(state = DISABLED)
	#reset the manager here
	manager.init_manager()

def reset():
	"""
	function to reset the program
	"""
	reset_pmem_view()
	reset_ptbl_view()
	for btn in buttons.keys():
		buttons[btn].config(state = NORMAL)
	manager.init_manager()

def quit_program():
	"""
	function to quit the program
	"""
	sys.exit(0)

########################   SET UP FRAMES    #############################
root = Tk()
root.title("Memory Management Simulation!!!")

#set up the main content frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#set up the labels frame for physical memory
phys_mem_labels_frame = ttk.Frame(mainframe, padding="3 3 12 12")
phys_mem_labels_frame.grid(column=0, row=0, sticky=(N, W, E, S))
phys_mem_labels_frame.rowconfigure(0, weight=1)

#set up the frames for the process page tables
for i in range(5):
	proc_table_frame = ttk.Frame(mainframe, padding="3 3 12 12")
	proc_table_frame.grid(column=i+1, row=0, sticky=(N, W, E, S))
	process_table_frames.append(proc_table_frame)


#set up the buttons frame along the bottom
buttons_frame = ttk.Frame(root, padding="3 3 12 12")
buttons_frame.grid(column=0, row=1, sticky=(N, W, E, S))
buttons_frame.columnconfigure(0, weight=1)

#######################   SET UP PHYSICAL MEMORY TABLE    ###############
def init_physicalm_view():
	#add the table headers
	phy_main_header = ttk.Label(phys_mem_labels_frame, text="PHYSICAL MEMORY")
	phy_main_header.grid(column=0, row=0, sticky=W, ipady=25)
	pid_header = ttk.Label(phys_mem_labels_frame, text="FRAME    PID   PAGE#")
	pid_header.grid(column=0, row=1, sticky=W, ipady=10)

	#add table cells here
	for i in range(16):
		if i < 10:
			pid_lab = ttk.Label(phys_mem_labels_frame, text="{}:          NULL,  NULL".format(i), relief=SUNKEN)
			pid_lab.grid(column=0, row=i+2, sticky=W, pady=3, padx=(0,25))
		else:
			pid_lab = ttk.Label(phys_mem_labels_frame, text="{}:        NULL,  NULL".format(i), relief=SUNKEN)
			pid_lab.grid(column=0, row=i+2, sticky=W, pady=3, padx=(0,25))
		#add for later update reference
		table_labels.append(pid_lab)

def reset_pmem_view():
	for i in range(16):
		if i < 10:
			table_labels[i]['text'] = "{}:          NULL,  NULL".format(i)
		else:
			table_labels[i]['text'] = "{}:        NULL,  NULL".format(i)


#######################   SET UP PROCESS TABLES    #######################
def init_ptables_view():
	for i in range(5): #set up 5 page tables
		#header labels for each page table
		page_tblmain_header = ttk.Label(process_table_frames[i], text="P{} PAGE TABLE".format(i+1))
		page_tblmain_header.grid(column=i+1, row=0, sticky=W, ipady=25)
		page_header = ttk.Label(process_table_frames[i], text="PAGE    FRAME   LRU")
		page_header.grid(column=i+1, row=1, sticky=W, ipady=10)

		for j in range(16): #set up logical addr space
			if j < 10:
				page_lab = ttk.Label(process_table_frames[i], text="{}:          NULL,  NULL".format(j), relief=SUNKEN)
				page_lab.grid(column=i+1, row=j+2, sticky=W, pady=3, padx=(0,25))
			else:
				page_lab = ttk.Label(process_table_frames[i], text="{}:        NULL,  NULL".format(j), relief=SUNKEN)
				page_lab.grid(column=i+1, row=j+2, sticky=W, pady=3, padx=(0,25))
			#add for later update reference
			if 'P{}:'.format(i+1) not in process_tables_labels.keys():
				process_tables_labels['P{}:'.format(i+1)] = [page_lab]
			else:
				process_tables_labels['P{}:'.format(i+1)].append(page_lab)

def reset_ptbl_view():
	for i in range(5):
		for j in range(16):
			if j < 10:
				process_tables_labels['P{}:'.format(i+1)][j]['text'] = "{}:          NULL,  NULL".format(j)
			else:
				process_tables_labels['P{}:'.format(i+1)][j]['text'] = "{}:        NULL,  NULL".format(j)

init_physicalm_view()
init_ptables_view()

########################   SET UP BUTTONS    #############################
#Run to completion button
run_to_complete_btn = ttk.Button(buttons_frame, text="Run To Completion" ,command=run_to_completion)
run_to_complete_btn.grid(column=0, row=0, sticky=(S, W))
buttons['Complete'] = run_to_complete_btn
#Run to next step button
run_to_next_btn = ttk.Button(buttons_frame, text="Run To Next Step",command=run_to_next_step)
run_to_next_btn.grid(column=1, row=0, sticky=(W))
buttons['Next'] = run_to_next_btn
#quit button
quit_btn = ttk.Button(buttons_frame, text="Quit", command=quit_program)
quit_btn.grid(column=3, row=0, sticky=(W))
buttons['Quit'] = quit_btn
#reset button
reset_btn = ttk.Button(buttons_frame, text="Reset Sim", command=reset)
reset_btn.grid(column=2, row=0, sticky=W)
buttons['Reset'] = reset_btn

root.mainloop()





