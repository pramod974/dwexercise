import os
import shutil
import threading
from random import randrange
import time
import MerkleTree as mt
import sys
#Class for heart simulator object

class heart_sim(object):

    def __init__(self,deploypath):
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
        self.deploy = threading.Event() # Threading event to run deployment ('t' sec interval)
        self.deploystat=0
        self.deploysource=deploypath
        self.trend = threading.Event() # Threading event to run fail machine command (1 sec interval)
        self.recovered_machines = []
        self.deployed = []
    # Remove exicting machines(directory) from the system
    def cleanup(self):
        for items in os.listdir(self.cd):
            if os.path.isdir(self.cd+"/"+items):
                shutil.rmtree(self.cd+"/"+items)

    # Function to create new_machines diretories		
    def init_machines(self):
        for num in xrange(self.num_machines):
            os.chdir(self.cd)
            machine = 'm_' + str(num)
            dirname = self.cd + "/" + machine
            self.m_list.append(dirname)
            os.mkdir(dirname)
            fp = dirname + "/" + self.fname
            open(fp, 'a').close()

    # Function to process raw input given by the user about the number of machines
    # fail percentage and Recovery time and set these to corresponding variables
    def set_vars(self):
        # print "Enter followed by space : Number of Machines, Fail Percentage and Recovery time(in sec)"
        lis = [500,10,5]
        self.num_machines = int(lis[0])
        self.fp = float(lis[1])
        self.rtime = int(lis[2])

    # Get a list of machines which are alive at the moment
    def get_alive_machines(self):
        alive_lis = []
        for items in os.listdir(self.cd):
            dirpath = self.cd + "/" + items
            if os.path.isdir(dirpath) == True:
                fpath = dirpath + "/" + self.fname
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
                    print "Failed ",machine
                    fpath = self.cd + "/" + machine + "/" + self.fname
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
                dirname = self.cd + "/" + item
                fp = dirname + "/" + self.fname
                open(fp, 'a').close()
                if item not in self.recovered_machines:
                    self.recovered_machines.append(item)
                    print "Recovered ",item
            self.failed_machines = []
            self.recover.wait(self.rtime)
            if self.recover.is_set():
                break
    #Function to verify the ddeployments
    def verify_deployment(self,dest):
        try:
            for item in os.listdir(self.deploysource):
                obj = mt.Diff(dest+"/"+item,self.deploysource+"/"+item)
                obj.make_trees()
                return obj.valid
        except Exception as e:
            print e
            return 0
    #function to deploy contents
    def deploy_contents(self,machines,place):
        for item in machines:
            dirname = self.cd + "/" + item
            fp = dirname + "/" + "deployedFiles"
            self.copy_and_overwrite(self.deploysource,fp)
            if self.verify_deployment(fp):
                self.deployed.append(item)
            print "Deployed ",place, item
            self.deploystat +=1
    #function to check and deploy every t seconds
    def deploy_recoverd_machine(self):
        while(True):
            #Deploy on "Recovered Failed Machines"
            print "*****************Deploy Recovered*********************"
            self.deploy_contents(set(self.recovered_machines)-set(self.deployed),"recovery")
            self.recovered_machines=[]
            self.deploy.wait(self.rtime)
            if self.deploystat == self.num_machines:
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
            fpath = items + "/" + self.fname
            if os.path.exists(fpath):
                    count +=1
        return count

    # Function to remove the Machine
    def remove_machines(self,mlis):
        for item in mlis:
            dirname = self.cd + "/" + item
            if os.path.exists(dirname):
                shutil.rmtree(dirname)
                self.m_list.remove(dirname)
                print "Machine " + item + " Removed"
            else:
                print "Machine " + item + " Does not exists"

    # Function to add new machines
    def add_machines(self,mlis):
        for item in mlis:
            dirname = self.cd + "/" + item
            if os.path.exists(dirname):
                print "Machine " + item + " Already exists"
            else:
                self.m_list.append(dirname)
                os.mkdir(dirname)
                fp = dirname + "/" + self.fname
                open(fp, 'a').close()
                print "Machine " + item + " Added"

    # Function to perform "is_alive" command
    def is_alive(self,machine):
        mpath = self.cd + "/" + machine
        if os.path.exists(mpath):
            fpath = mpath + "/" + self.fname
            if os.path.exists(fpath):
                print True
            else:
                print False
        else:
            print "Machine Not Present"

    # Function to print the failure_trend report (per second basis)
    def failure_trends(self):
        print self.trendlis
    def copy_and_overwrite(self,from_path,to_path):
        if os.path.exists(to_path):
            shutil.rmtree(to_path)
        shutil.copytree(from_path, to_path)
    # Wrapper to simulate the heart beat monitoring system
    def execute(self):
        self.set_vars()
        self.init_machines()
        t = threading.Timer(1,self.fail_machine)
        t.start()

        rm = threading.Timer(1,self.recover_machine)
        rm.start()
        tr = threading.Timer(1,self.calculate_trend)
        tr.start()
        time.sleep(5)
        alive=self.get_alive_machines()
        self.deploy_contents(set(alive)-set(self.deployed),"alive")
        drm= threading.Timer(1,self.deploy_recoverd_machine)
        drm.start()
        while True:
            pass
            if self.deploystat == self.num_machines:
                break
        self.fail.set()
        self.recover.set()
        self.deploy.set()
        self.trend.set()
        t.cancel()
        rm.cancel()
        tr.cancel()
        drm.cancel()
        self.cleanup()

        print 'Thanks for using system'


if len(sys.argv)>1:
    if os.path.exists(sys.argv[1]):
        ob = heart_sim(sys.argv[1])
        ob.execute()
    else:
        print "Please send a VALID Path to files that has to be deployed"
else:
    print "Please send Path to files that has to be deployed"
