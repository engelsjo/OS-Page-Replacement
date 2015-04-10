from Tkinter import *
from _tkinter import *
import ttk as ttk
from memory_manager import memory_manager

########################   Create Instance of Model   ###################
manager = memory_manager()

#### place global vars here
table_labels = []

########################   Controller methods for updating view #########

def update_pmemory_tbl():
	"""
	function that updates the physical memory table
	"""
	manager.manage()
	for i, frame in enumerate(manager.physical_memory):
		table_labels[i][0]['text'] = frame[0]
		table_labels[i][1]['text'] = frame[1] 

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
phys_mem_labels_frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=(10, 20))
phys_mem_labels_frame.rowconfigure(0, weight=2)

#set up the buttons frame along the bottom
buttons_frame = ttk.Frame(mainframe, padding="3 3 12 12")
buttons_frame.grid(column=0, row=1, sticky=(N, W, E, S), pady=(50, 10))

table_frame = ttk.Frame(mainframe, padding="3 3 12 12")
table_frame.grid(column=1, row=0, stick=(N, W, E, S))

########################   SET UP LABELS    #############################
phys_mem_lab = ttk.Label(phys_mem_labels_frame, text="Frame Number")
phys_mem_lab.grid(column=0, row=0, sticky=W, ipady=25)

for i in range(16):
	frame_lab = ttk.Label(phys_mem_labels_frame, text="Frame: {}".format(i))
	frame_lab.grid(column=0, row=i+1, sticky=W, pady=3)

########################   SET UP PHYSICAL MEMORY TABLE    ###############
#add the table headers
pid_header = ttk.Label(table_frame, text="Process")
pid_header.grid(column=0, row=0, sticky=W, ipady=25)
page_header = ttk.Label(table_frame, text="Page Number")
page_header.grid(column=1, row=0, sticky=W, ipady=25)

for i in range(16):
	#add the pid here
	pid_lab = ttk.Label(table_frame, text="NULL")
	pid_lab.grid(column=0, row=i+1, sticky=W, pady=3, padx=(0,25))

	#add the page column label
	page_lab = ttk.Label(table_frame, text="NULL")
	page_lab.grid(column=1, row=i+1, sticky=W, pady=3)

	#add for later update reference
	table_labels.append((pid_lab, page_lab))


########################   SET UP BUTTONS    #############################
#Run to completion button
run_to_complete_btn = ttk.Button(buttons_frame, text="Run To Completion", command=update_pmemory_tbl)
run_to_complete_btn.grid(column=0, row=17, sticky=(S, W))

root.mainloop()