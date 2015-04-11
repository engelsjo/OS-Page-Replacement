from Tkinter import *
from _tkinter import *
import ttk as ttk
from memory_manager import memory_manager
import sys

########################   Create Instance of Model   ###################
manager = memory_manager()

#### place global vars here
table_labels = []
buttons = {}

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


def run_to_completion():
	"""
	function that executes the entire data file
	""" 
	#update the model
	manager.runToCompletion()
	#update the view
	update_pmemory_tbl()
	#disable buttons
	for btn in buttons.keys():
		if btn != "Quit":
			buttons[btn].config(state = DISABLED)
	#reset the manager here
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

#set up the buttons frame along the bottom
buttons_frame = ttk.Frame(root, padding="3 3 12 12")
buttons_frame.grid(column=0, row=1, sticky=(N, W, E, S))
buttons_frame.columnconfigure(0, weight=1)

#######################   SET UP PHYSICAL MEMORY TABLE    ###############
#add the table headers
phy_main_header = ttk.Label(phys_mem_labels_frame, text="PHYSICAL MEMORY")
phy_main_header.grid(column=0, row=0, sticky=W, ipady=25)
pid_header = ttk.Label(phys_mem_labels_frame, text="FRAME    PID   PAGE#")
pid_header.grid(column=0, row=1, sticky=W, ipady=10)

for i in range(16):
	#add the pid here
	if i < 10:
		pid_lab = ttk.Label(phys_mem_labels_frame, text="{}:          NULL,  NULL".format(i), relief=SUNKEN)
		pid_lab.grid(column=0, row=i+2, sticky=W, pady=3, padx=(0,25))
	else:
		pid_lab = ttk.Label(phys_mem_labels_frame, text="{}:        NULL,  NULL".format(i), relief=SUNKEN)
		pid_lab.grid(column=0, row=i+2, sticky=W, pady=3, padx=(0,25))
	#add for later update reference
	table_labels.append(pid_lab)


########################   SET UP BUTTONS    #############################
#Run to completion button
run_to_complete_btn = ttk.Button(buttons_frame, text="Run To Completion" ,command=run_to_completion)
run_to_complete_btn.grid(column=0, row=0, sticky=(S, W))
buttons['Complete'] = run_to_complete_btn
#Run to next step button
run_to_next_btn = ttk.Button(buttons_frame, text="Run To Next Step",command=run_to_next_step)
run_to_next_btn.grid(column=1, row=0, sticky=(S, W))
buttons['Next'] = run_to_next_btn
#quit button
quit_btn = ttk.Button(buttons_frame, text="Quit", command=quit_program)
quit_btn.grid(column=2, row=0, sticky=(S, W))
buttons['Quit'] = quit_btn

root.mainloop()





