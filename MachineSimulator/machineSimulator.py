import os
import shutil
import threading
from random import randrange

#Class for heart simulator object

class heart_sim(object):

    def __init__(self):
        self.num_machine = 0
        self.fp = 0 # fail percentage
        self.rtime = 0 # recovery time (set afterwords)
        self.ftime = 5 # fail time
        self.cd = os.getcwd()+"/machines" # current directory
        self.m_list = [] # list of machines at present
        self.fname = "Alive" #file name to be added/ remove from machine 
        self.cleanup() #Remove all the directories for a fresh run
        self.trendlis = [] #List to maintain the trend report (no of machines alive till now)
        self.failed_machines = [] # List of failed machines
        self.fail = threading.Event() # Threading event to run fail machine command (5 sec interval)
        self.recover = threading.Event() # Threading event to run recover machine command ('t' sec interval)
        self.trend = threading.Event() # Threading event to run fail machine command (1 sec interval)

    # Remove exicting machines(directory) from the system
    def cleanup(self):
        for items in os.listdir(self.cd):
            if os.path.isdir(items):
                shutil.rmtree(items)

    # Function to create new_machines diretories		
    def init_machines(self):
        for num in xrange(self.num_machines):
            os.chdir(self.cd)
            machine = 'm_' + str(num)
            dirname = self.cd + '/' + machine
            self.m_list.append(dirname)
            os.mkdir(dirname)
            fp = dirname + '/' + self.fname
            open(fp, 'a').close()

    # Function to process raw input given by the user about the number of machines
    # fail percentage and Recovery time and set these to corresponding variables
    def set_vars(self):
        print "Enter Number of Machines, Fail Percentage and Recovery time(in sec)"
        lis = []
        while len(lis) != 3:
            print "please enter values in correct format"
            string = raw_input()
            lis = string.split(' ')
        self.num_machines = int(lis[0])
        self.fp = float(lis[1])
        self.rtime = int(lis[2])

    # Get a list of machines which are alive at the moment
    def get_alive_machines(self):
        alive_lis = []
        for items in os.listdir(self.cd):
            dirpath = self.cd + '/' + items
            if os.path.isdir(dirpath) == True:
                fpath = dirpath + '/' + self.fname
                if os.path.exists(fpath):
                    alive_lis.append(items)
        return alive_lis
    
    # Function to chooses N * f directories (machines) randomly and delete the 'alive' file from
    # them to indicate that those machines are not alive
    def fail_machine(self):
        while(True):
            #print "hello"
            num_failed = int(self.num_machines * self.fp/100.0)
            count = 0
            alive_lis = self.get_alive_machines()
            length = len(alive_lis)
            while num_failed != 0:
                try:
                    index = randrange(length)
                    machine = alive_lis[index]
                    self.failed_machines.append(machine)
                    fpath = self.cd + '/' + machine + '/' + self.fname
                    if os.path.exists(fpath):
                        os.remove(fpath)
                    num_failed -= 1
                except:
                    pass    
            self.fail.wait(self.ftime)
            if self.fail.is_set():
                break

    # Function to simulate the recovery process it
    # recreate the 'alive' file in all the failed machines.    
    def recover_machine(self):
	while(True):
	    #print "Recovered Failed Machines"
	    for item in self.failed_machines:
		dirname = self.cd + '/' + item
	        fp = dirname + '/' + self.fname
	        open(fp, 'a').close()

	    self.failed_machines = []
	    self.recover.wait(self.rtime)
	    if self.recover.is_set():
		break

    # Function to do fail_trend analysis
    def calculate_trend(self):
	while(True):
	    curr_alive = self.check_machines()
	    self.trendlis.append(curr_alive)
	    self.trend.wait(1)
	    if self.trend.is_set():
		break

    # Function to find the number of alive machine at the moment
    def check_machines(self):
        count = 0
	for items in os.listdir(self.cd):
	    fpath = items + '/' + self.fname
	    if os.path.exists(fpath):
    	        count +=1
	return count

    # Function to remove the Machine
    def remove_machines(self,mlis):
	for item in mlis:
	    dirname = self.cd + '/' + item
	    if os.path.exists(dirname):
		shutil.rmtree(dirname)
		self.m_list.remove(dirname)
		print "Machine " + item + " Removed"
	    else:
		print "Machine " + item + " Does not exists"

    # Function to add new machines
    def add_machines(self,mlis):
	for item in mlis:
	    dirname = self.cd + '/' + item
	    if os.path.exists(dirname):
		print "Machine " + item + " Already exists"
	    else:
                self.m_list.append(dirname)
	        os.mkdir(dirname)
	        fp = dirname + '/' + self.fname
	        open(fp, 'a').close()
		print "Machine " + item + " Added"

    # Function to perform "is_alive" command
    def is_alive(self,machine):
	mpath = self.cd + '/' + machine
	if os.path.exists(mpath):
	    fpath = mpath + '/' + self.fname	
	    if os.path.exists(fpath):
	        print True
	    else:
	        print False
	else:
	    print "Machine Not Present"

    # Function to print the failure_trend report (per second basis)
    def failure_trends(self):
	print self.trendlis

    # Wrapper to simulate the heart beat monitoring system
    def execute(self):
	self.set_vars()
	self.init_machines()
	t = threading.Timer(5,self.fail_machine)
	rm = threading.Timer(5,self.recover_machine)
	tr = threading.Timer(5,self.calculate_trend)
        t.start()
	rm.start()
	tr.start()
	command = ''
	while command != 'quit':
	    print """ Please Enter your choice:
1.failure_trend
2. is_machine_alive m_4
3. remove_machines m_4
4. num_machines_alive
5. add_machines m_1,m_3
6. Type quit to exit
"""
	    command = raw_input()
	    if command == "num_machines_alive":
		print self.check_machines()

	    elif 'add_machines' in command:
		machines = command.split(' ')[1]
		machines = machines.split(',')
		self.add_machines(machines)

	    elif 'remove_machines' in command:
		machines = command.split(' ')[1]
		machines = machines.split(',')
		self.remove_machines(machines)

	    elif 'is_machine_alive' in command:
		machine = command.split(' ')[1]
		self.is_alive(machine)

	    elif command == 'failure_trend':
		self.failure_trends()

	    elif command == 'quit':
		self.fail.set()
		self.recover.set()
		self.trend.set()
		t.cancel()
		rm.cancel()
		tr.cancel()
		self.cleanup()
		print 'Thanks for using system'
	    else:
		print "Please enter the correct Choice"

