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
sim_status_label = ''
stats_labels = []

########################   Controller methods for updating view #########

def update_pmemory_tbl():
	"""
	function that updates the physical memory table
	"""
	for i, frame in enumerate(manager.physical_memory):
		if frame != -1:
			if i < 10:
				r_time = manager.pcb_records[frame[0]].page_table[frame[1]][1].strftime("%I:%M:%S:%f")
				if frame[1] < 10:
					table_labels[i]['text'] = "{}:   {}     {}    {}".format(i, frame[0], frame[1], r_time)
				else:
					table_labels[i]['text'] = "{}:   {}   {}    {}".format(i, frame[0], frame[1], r_time)
			else:
				if frame[1] < 10:
					table_labels[i]['text'] = "{}: {}     {}    {}".format(i, frame[0], frame[1], r_time)
				else:
					table_labels[i]['text'] = "{}: {}   {}    {}".format(i, frame[0], frame[1], r_time)
			table_labels[i]['background'] = "gray"

def update_page_tables():
	"""
	function that updates the page tables
	"""
	for pcb in manager.pcb_records:
		page_table = manager.pcb_records[pcb].page_table
		for page, page_info in sorted(page_table.iteritems()):
			rbit = "1" if page_info[2] else "0"
			if page > 9 and page_info[0] > 9:
				row_text = "{}:     {}       {}        {}".format(page, page_info[0], rbit, page_info[1].strftime("%I:%M:%S"))
			elif page > 9:
				row_text = "{}:     {}         {}        {}".format(page, page_info[0], rbit, page_info[1].strftime("%I:%M:%S"))
			elif page_info[0] > 9:
				row_text = "{}:       {}       {}        {}".format(page, page_info[0], rbit, page_info[1].strftime("%I:%M:%S"))
			else:
				row_text = "{}:       {}         {}        {}".format(page, page_info[0], rbit, page_info[1].strftime("%I:%M:%S"))
			process_tables_labels[pcb][page]['text'] = row_text
			process_tables_labels[pcb][page]['background'] = "gray"

def update_stats():
	"""
	function to update the statistics
	"""
	i = 1
	total_refs = 0
	total_faults = 0
	for pcb in sorted(manager.pcb_records):
		refs_made = manager.pcb_records[pcb].mem_references_made
		faults = manager.pcb_records[pcb].number_of_faults
		total_refs += refs_made
		total_faults += faults
		stats_labels[i]['text'] = "{} Faults: {}\nReferences: {}".format(pcb, faults, refs_made)
		i += 1
	stats_labels[0]['text'] = "Total Faults: {}\n Total References: {}".format(total_faults, total_refs)

def hightlight_changes():
	"""
	function that highlights changes made to page table and physical memory table.
	Parses status text to determine changes to high-light to user
	"Simulation Status: {} requested page {}. Page Fault occurred. Frame {} granted"
	"""
	if "COMPLETE," in manager.status:
		return
	elif "Page Fault" in manager.status:
		status_parts = manager.status.split()
		pid = status_parts[2]
		page_nbr = int(status_parts[5][0])
		frame_nbr = int(status_parts[10])
		table_labels[frame_nbr]['background'] = "red"
		process_tables_labels[pid][page_nbr]['background'] = 'red'
	else: #memory reference
		status_parts = manager.status.split()
		pid = status_parts[2]
		page_nbr = int(status_parts[5][0])
		frame_nbr = int(status_parts[13])
		table_labels[frame_nbr]['background'] = 'green'
		process_tables_labels[pid][page_nbr]['background'] = 'green'

def update_sim_status():
	"""
	function that updates the simulation status
	"""
	#print(manager.last_vict)
	if manager.last_vict != "" and "COMPLETE" not in manager.status:
		sim_status_label['text'] = "{}. LRU Victim: {} page {}".format(manager.status, manager.last_vict[0], manager.last_vict[1])
		manager.last_vict = ""
	else:
		sim_status_label['text'] = manager.status

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
	update_sim_status()
	hightlight_changes()
	update_stats()
	if manager.curr_ref_index == len(manager.file_contents):
		for btn in buttons.keys():
			if btn != "Quit" and btn != "Reset":
				buttons[btn].config(state = DISABLED)
		#reset the manager here
		manager.init_manager()


def run_to_completion():
	"""
	function that executes the entire data file
	""" 
	#update the model
	manager.runToCompletion()
	#update the view
	update_pmemory_tbl()
	update_page_tables()
	update_sim_status()
	hightlight_changes
	update_stats()
	#disable buttons
	for btn in buttons.keys():
		if btn != "Quit" and btn != "Reset":
			buttons[btn].config(state = DISABLED)
	#reset the manager here
	manager.init_manager()

def run_to_next_pg_fault():
	"""
	function that executes the references up to the next page fault
	"""
	manager.status = "" #clear status
	manager.runToFault()
	#update the view
	update_pmemory_tbl()
	update_page_tables()
	update_sim_status()
	hightlight_changes()
	update_stats()
	if manager.curr_ref_index == len(manager.file_contents):
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
	reset_stats()
	for btn in buttons.keys():
		buttons[btn].config(state = NORMAL)
	manager.init_manager()
	update_sim_status()

def quit_program():
	"""
	function to quit the program
	"""
	sys.exit(0)

########################   VIEW CODE -- SET UP FRAMES    #############################
root = Tk()
root.title("Memory Management Simulation!!!")

#set up the main content frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)

#set up the labels frame for physical memory
phys_mem_labels_frame = ttk.Frame(mainframe, padding="3 3 12 12")
phys_mem_labels_frame.grid(column=0, row=0, sticky=(N, W, E, S))
phys_mem_labels_frame.rowconfigure(0, weight=1)

#set up the frames for the process page tables
for i in range(5):
	proc_table_frame = ttk.Frame(mainframe, padding="3 3 12 12")
	proc_table_frame.grid(column=i+1, row=0, sticky=(N, W, E, S))
	process_table_frames.append(proc_table_frame)

statistics_frame = ttk.Frame(root, padding="3 3 12 12")
statistics_frame.grid(column=0, row=1, sticky=(N, W, E, S))

#set up the game status frame
status_frame = ttk.Frame(root, padding="3 3 12 12")
status_frame.grid(column=0 ,row=2, sticky=(N, W, E, S))

#set up the buttons frame along the bottom
buttons_frame = ttk.Frame(root, padding="3 3 12 12")
buttons_frame.grid(column=0, row=3, sticky=(N, W, E, S))

#######################   SET UP PHYSICAL MEMORY TABLE    ###############
def init_physicalm_view():
	#add the table headers
	phy_main_header = ttk.Label(phys_mem_labels_frame, text="PHYSICAL MEMORY")
	phy_main_header.grid(column=0, row=0, sticky=W, ipady=25)
	pid_header = ttk.Label(phys_mem_labels_frame, text="F#  PID   PAGE#     RTime")
	pid_header.grid(column=0, row=1, sticky=W, ipady=10)

	#add table cells here
	for i in range(16):
		if i < 10:
			pid_lab = ttk.Label(phys_mem_labels_frame, text="{}:                                               ".format(i), relief=SUNKEN)
			pid_lab.grid(column=0, row=i+2, sticky=W, pady=3, padx=(0,25))
		else:
			pid_lab = ttk.Label(phys_mem_labels_frame, text="{}:                                             ".format(i), relief=SUNKEN)
			pid_lab.grid(column=0, row=i+2, sticky=W, pady=3, padx=(0,25))
		#add for later update reference
		pid_lab['background'] = "gray"
		table_labels.append(pid_lab)

def reset_pmem_view():
	for i in range(16):
		if i < 10:
			table_labels[i]['text'] = "{}:                                               ".format(i)
		else:
			table_labels[i]['text'] = "{}:                                             ".format(i)
		table_labels[i]['background'] = "gray"


#######################   SET UP PROCESS TABLES    #######################
def init_ptables_view():
	for i in range(5): #set up 5 page tables
		#header labels for each page table
		page_tblmain_header = ttk.Label(process_table_frames[i], text="P{} PAGE TABLE".format(i+1))
		page_tblmain_header.grid(column=i+1, row=0, sticky=W, ipady=25)
		page_header = ttk.Label(process_table_frames[i], text="PG    F#     R-Bit     RTime")
		page_header.grid(column=i+1, row=1, sticky=W, ipady=10)

		for j in range(16): #set up logical addr space
			if j < 10:
				page_lab = ttk.Label(process_table_frames[i], text="{}:                                          ".format(j), relief=SUNKEN)
				page_lab.grid(column=i+1, row=j+2, sticky=W, pady=3, padx=(0,25))
			else:
				page_lab = ttk.Label(process_table_frames[i], text="{}:                                        ".format(j), relief=SUNKEN)
				page_lab.grid(column=i+1, row=j+2, sticky=W, pady=3, padx=(0,25))
			#add for later update reference
			page_lab['background'] = "gray"
			if 'P{}:'.format(i+1) not in process_tables_labels.keys():
				process_tables_labels['P{}:'.format(i+1)] = [page_lab]
			else:
				process_tables_labels['P{}:'.format(i+1)].append(page_lab)

def reset_ptbl_view():
	for i in range(5):
		for j in range(16):
			process_tables_labels['P{}:'.format(i+1)][j]['background'] = "gray"
			if j < 10:
				process_tables_labels['P{}:'.format(i+1)][j]['text'] = "{}:                                          ".format(j)
			else:
				process_tables_labels['P{}:'.format(i+1)][j]['text'] = "{}:                                        ".format(j)

init_physicalm_view()
init_ptables_view()

########################   SET UP STATS     #############################
#page faults
pad_val = (0, 140)
tot_faults_lab = ttk.Label(statistics_frame, text="Total Faults: 0\nTotal References: 000")
tot_faults_lab.grid(row=0, column=0, padx=pad_val)
p1_faults = ttk.Label(statistics_frame, text="P1 Faults: 0\nReferences: 000")
p1_faults.grid(row=0, column=1, padx=(0,115))
p2_faults = ttk.Label(statistics_frame, text="P2 Faults: 0\nReferences: 000")
p2_faults.grid(row=0, column=2, padx=(0,110))
p3_faults = ttk.Label(statistics_frame, text="P3 Faults: 0\nReferences: 000")
p3_faults.grid(row=0, column=3, padx=(0,105))
p4_faults = ttk.Label(statistics_frame, text="P4 Faults: 0\nReferences: 000")
p4_faults.grid(row=0, column=4, padx=(0,105))
p5_faults = ttk.Label(statistics_frame, text="P5 Faults: 0\nReferences: 000")
p5_faults.grid(row=0, column=5)
stats_labels = [tot_faults_lab, p1_faults, p2_faults, p3_faults, p4_faults, p5_faults]

def reset_stats():
	stats_labels[0]['text'] = "Total Faults: 0\nTotal Ref: 000"
	for i in range(len(stats_labels)):
		if i != 0:
			stats_labels[i]['text'] = "P{} Faults: 0\nReferences: 000".format(i)



########################   SET UP STATUS     #############################
sim_status_label = ttk.Label(status_frame, text="Simulation Status: Welcome to VM Simulation")
sim_status_label.grid(column=0, row=0)

########################   SET UP BUTTONS    #############################
#Run to completion button
run_to_complete_btn = ttk.Button(buttons_frame, text="Run To Completion" ,command=run_to_completion)
run_to_complete_btn.grid(column=0, row=0, sticky=(W))
buttons['Complete'] = run_to_complete_btn
#Run to next page fault button
run_to_fault_btn = ttk.Button(buttons_frame, text="Run To Next Page Fault",command=run_to_next_pg_fault)
run_to_fault_btn.grid(column=1, row=0, sticky=(W))
buttons['Fault'] = run_to_fault_btn
#Run to next step button
run_to_next_btn = ttk.Button(buttons_frame, text="Run To Next Reference",command=run_to_next_step)
run_to_next_btn.grid(column=2, row=0, sticky=(W))
buttons['Next'] = run_to_next_btn
#quit button
quit_btn = ttk.Button(buttons_frame, text="Quit", command=quit_program)
quit_btn.grid(column=4, row=0, sticky=(E))
buttons['Quit'] = quit_btn
#reset button
reset_btn = ttk.Button(buttons_frame, text="Reset Sim", command=reset)
reset_btn.grid(column=3, row=0, sticky=E)
buttons['Reset'] = reset_btn

root.mainloop()





